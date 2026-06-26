"""Scales selected objects dynamically and exclusively along the Z-axis, with real-time preview and snapping capabilities."""

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore
import System  # type: ignore

__commandname__ = "knScaleZ" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

# This class handles the real-time math while the mouse is moving
class InteractiveZScale(Rhino.Input.Custom.GetTransform):
    def __init__(self, base_pt, ref_pt):
        # === THE FIX ===
        # We MUST explicitly initialize the base Rhino class, otherwise 
        # the internal graphics engine never wakes up to draw the ghosted preview!
        Rhino.Input.Custom.GetTransform.__init__(self)
        # ===============
        
        # Define starting variables
        self.base_pt = base_pt
        self.ref_pt = ref_pt
        
        # Calculate initial Z difference
        self.dz0 = ref_pt.Z - base_pt.Z
        
        # Prevent mathematical error if the user clicks a perfectly flat reference point
        if abs(self.dz0) < 1e-8:
            self.dz0 = 1e-8

    # This function triggers constantly during the mouse drag to scale the geometry
    def CalculateTransform(self, viewport, point):
        # Calculate new Z difference based on current mouse location
        dz1 = point.Z - self.base_pt.Z
        factor = dz1 / self.dz0
        
        # Build a Plane at the base point to serve as our axis lock
        plane = Rhino.Geometry.Plane(self.base_pt, Rhino.Geometry.Vector3d.ZAxis)
        
        # Generate the live transform: X=1.0, Y=1.0, Z=Dynamic Factor
        xform = Rhino.Geometry.Transform.Scale(plane, 1.0, 1.0, factor)
        return xform
        
    def OnDynamicDraw(self, e):
        # Draw a dotted line from the base to the original reference point
        e.Display.DrawDottedLine(self.base_pt, self.ref_pt, System.Drawing.Color.DarkGray)
        # Call the base class method so Rhino draws the ghosted objects based on CalculateTransform
        Rhino.Input.Custom.GetTransform.OnDynamicDraw(self, e)

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # 1. Get objects
    objects = rs.GetObjects("Select objects to dynamically scale in Z-axis", preselect=True)
    if not objects: return 1
    
    # 2. Get the Origin/Base point
    base_pt = rs.GetPoint("Origin point")
    if not base_pt: return 1
    
    # 3. Get the first reference point
    ref_pt = rs.GetPoint("Reference point for first scale factor", base_pt)
    if not ref_pt: return 1
    
    # Initialize our custom RhinoCommon dynamic tracker
    tracker = InteractiveZScale(base_pt, ref_pt)
    
    # Create the specialized list container that Rhino requires
    xform_list = Rhino.Collections.TransformObjectList()
    
    # Load the selected objects into the list
    for obj_id in objects:
        rhino_obj = sc.doc.Objects.Find(obj_id)
        if rhino_obj:
            xform_list.Add(rhino_obj)
            
    # Add the entire list to the tracker so they "ghost" in real-time
    tracker.AddTransformObjects(xform_list)
            
    tracker.SetCommandPrompt("Target point (snapping will only use Z-elevation)")
    tracker.SetBasePoint(base_pt, True) 
    
    # 4. Trigger the interactive drag phase
    tracker.Get()
    
    if tracker.CommandResult() != Rhino.Commands.Result.Success:
        return 1
        
    # Calculate the final math once the user clicks their target
    final_xform = tracker.CalculateTransform(tracker.View().ActiveViewport, tracker.Point())
    
    # Apply the final transform to the actual objects
    for obj_id in objects:
        sc.doc.Objects.Transform(obj_id, final_xform, True)
        
    sc.doc.Views.Redraw()
    return 0

RunCommand(True)