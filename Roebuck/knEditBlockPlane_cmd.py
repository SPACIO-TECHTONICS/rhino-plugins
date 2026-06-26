import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore
import System.Drawing.Color as Color  # type: ignore

__commandname__ = "knEditBlockPlane"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    # 1. Select block instance
    instance_id = rs.GetObject("Select a block instance to edit its reference plane", rs.filter.instance)
    if( instance_id == None ):
        return 1
        
    block_name = rs.BlockInstanceName(instance_id)
    instance_xform = rs.BlockInstanceXform(instance_id)
    
    # 2. Get NEW reference plane origin using RhinoCommon
    gp_origin = Rhino.Input.Custom.GetPoint()
    gp_origin.SetCommandPrompt("Select NEW reference plane origin (base point)")
    gp_origin.Get()
    if gp_origin.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    origin = gp_origin.Point()
        
    # 3. Get X-axis point
    gp_x = Rhino.Input.Custom.GetPoint()
    gp_x.SetCommandPrompt("Select a point on the NEW reference plane's X-axis")
    gp_x.SetBasePoint(origin, True)
    gp_x.DrawLineFromPoint(origin, True)
    gp_x.Get()
    if gp_x.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    x_pt = gp_x.Point()

    # Dynamic Draw function to visualize the plane in real-time
    def GetYPointDynamicDraw(sender, e):
        current_pt = e.CurrentPoint
        xaxis = x_pt - origin
        yaxis = current_pt - origin
        
        if xaxis.IsTiny(1e-6) or yaxis.IsTiny(1e-6) or xaxis.IsParallelTo(yaxis) != 0:
            return

        temp_plane = Rhino.Geometry.Plane(origin, xaxis, yaxis)
        
        e.Display.DrawLine(origin, origin + temp_plane.XAxis * xaxis.Length, Color.Red, 2)
        e.Display.DrawLine(origin, origin + temp_plane.YAxis * yaxis.Length, Color.Green, 2)
        e.Display.DrawLine(origin, origin + temp_plane.ZAxis * ((xaxis.Length + yaxis.Length) * 0.25), Color.Blue, 2)
        
        size_x = xaxis.Length
        size_y = yaxis.Length
        corners = [
            origin + temp_plane.XAxis * size_x + temp_plane.YAxis * size_y,
            origin - temp_plane.XAxis * size_x + temp_plane.YAxis * size_y,
            origin - temp_plane.XAxis * size_x - temp_plane.YAxis * size_y,
            origin + temp_plane.XAxis * size_x - temp_plane.YAxis * size_y,
            origin + temp_plane.XAxis * size_x + temp_plane.YAxis * size_y
        ]
        e.Display.DrawPolyline(corners, Color.DarkGray, 1)

    # 4. Get Y-axis point with dynamic draw
    gp_y = Rhino.Input.Custom.GetPoint()
    gp_y.SetCommandPrompt("Select a point on the NEW reference plane's Y-axis")
    gp_y.SetBasePoint(origin, True)
    gp_y.DynamicDraw += GetYPointDynamicDraw
    gp_y.Get()
    if gp_y.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    y_pt = gp_y.Point()

    world_plane = rs.PlaneFromPoints(origin, x_pt, y_pt)
    if( world_plane == None ):
        print("Invalid points selected for plane.")
        return 1

    # 5. Calculate transformations
    rc, inv_xform = instance_xform.TryGetInverse()
    if not rc: 
        print("Failed to invert instance transform.")
        return 1
        
    local_plane = world_plane.Clone()
    local_plane.Transform(inv_xform)

    xform_def = Rhino.Geometry.Transform.ChangeBasis(Rhino.Geometry.Plane.WorldXY, local_plane)
    xform_inst_offset = Rhino.Geometry.Transform.ChangeBasis(local_plane, Rhino.Geometry.Plane.WorldXY)

    # 6. Modify the block definition geometry
    idef = sc.doc.InstanceDefinitions.Find(block_name)
    if not idef: 
        return 1
    
    idef_objects = idef.GetObjects()
    geometry = []
    attributes = []
    for obj in idef_objects:
        geom = obj.Geometry.Duplicate()
        geom.Transform(xform_def)
        geometry.append(geom)
        attributes.append(obj.Attributes.Duplicate())
        
    sc.doc.InstanceDefinitions.ModifyGeometry(idef.Index, geometry, attributes)
    
    # 7. Update all instances to preserve their world locations
    instances = idef.GetReferences(1) 
    for inst in instances:
        old_xform = inst.InstanceXform
        new_xform = old_xform * xform_inst_offset
        rc, inv_old = old_xform.TryGetInverse()
        if rc:
            delta_xform = new_xform * inv_old
            rs.TransformObject(inst.Id, delta_xform, copy=False)

    sc.doc.Views.Redraw()

    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

if __name__ == "__main__":
    RunCommand(True)
