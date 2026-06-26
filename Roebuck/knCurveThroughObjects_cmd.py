"""Draws an interpolated curve directly through the bottom-center or top-center bounding box points of selected objects in their exact selection order."""

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knCurveThroughObjects" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # 1. Get objects (Selecting sequentially determines the flow of the curve)
    objects = rs.GetObjects("Select objects in the exact order you want the curve to flow", preselect=True)
    if not objects: return 1
    
    if len(objects) < 2:
        print "You must select at least two objects to draw a curve."
        return 1
        
    # 2. Check memory for previous alignment preference
    default_align = "BottomCenter"
    if sc.sticky.has_key("knCurveThroughObjects_LastAlign"):
        default_align = sc.sticky["knCurveThroughObjects_LastAlign"]
        
    # 3. Ask user for alignment
    alignment = rs.GetString("Curve path alignment", default_align, ["BottomCenter", "TopCenter"])
    if not alignment: return 1
    
    # Save the preference for next time
    sc.sticky["knCurveThroughObjects_LastAlign"] = alignment
        
    rs.EnableRedraw(False)
    points = []
    
    # 4. Extract the specified center point from each object
    for obj in objects:
        bbox = rs.BoundingBox(obj)
        if not bbox: continue
        
        # Calculate X and Y center of the bounding box
        center_x = (bbox[0].X + bbox[2].X) / 2.0
        center_y = (bbox[0].Y + bbox[2].Y) / 2.0
        
        # Apply Top vs Bottom logic based on user selection
        if alignment.lower() == "topcenter":
            target_z = bbox[4].Z # bbox[4] contains the top-most Z elevation
        else:
            target_z = bbox[0].Z # bbox[0] contains the bottom-most Z elevation
        
        base_pt = [center_x, center_y, target_z]
        points.append(base_pt)
        
    # 5. Draw the interpolated curve through the collected points
    if len(points) >= 2:
        # AddInterpCurve guarantees the curve passes directly THROUGH the points 
        curve = rs.AddInterpCurve(points)
        
        if curve:
            rs.SelectObject(curve) # Highlight the new curve for the user
            print "Successfully generated {} interpolated curve through {} object centers.".format(alignment, len(points))
        else:
            print "Failed to generate curve."
    else:
        print "Not enough valid object bounding boxes found."
        
    rs.EnableRedraw(True)
    
    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

RunCommand(True)