import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
import System.Drawing.Color as Color  # type: ignore

__commandname__ = "knCreateBlock" 

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    # get objects
    object_ids = rs.GetObjects("Select objects to define block", preselect=True)
    if( object_ids == None ):
        return 1

    # 1. Get reference plane origin using RhinoCommon
    gp_origin = Rhino.Input.Custom.GetPoint()
    gp_origin.SetCommandPrompt("Select reference plane origin (base point)")
    gp_origin.Get()
    if gp_origin.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    origin = gp_origin.Point()
        
    # 2. Get X-axis point with a simple tracking line
    gp_x = Rhino.Input.Custom.GetPoint()
    gp_x.SetCommandPrompt("Select a point on the reference plane's X-axis")
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
        
        # Prevent crash if points are coincident or collinear
        if xaxis.IsTiny(1e-6) or yaxis.IsTiny(1e-6) or xaxis.IsParallelTo(yaxis) != 0:
            return

        # Calculate the temporary plane
        temp_plane = Rhino.Geometry.Plane(origin, xaxis, yaxis)
        
        # Draw RGB axes
        e.Display.DrawLine(origin, origin + temp_plane.XAxis * xaxis.Length, Color.Red, 2)
        e.Display.DrawLine(origin, origin + temp_plane.YAxis * yaxis.Length, Color.Green, 2)
        e.Display.DrawLine(origin, origin + temp_plane.ZAxis * ((xaxis.Length + yaxis.Length) * 0.25), Color.Blue, 2)
        
        # Draw a rectangle to visualize the plane surface
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

    # 3. Get Y-axis point with the dynamic plane preview attached
    gp_y = Rhino.Input.Custom.GetPoint()
    gp_y.SetCommandPrompt("Select a point on the reference plane's Y-axis")
    gp_y.SetBasePoint(origin, True)
    gp_y.DynamicDraw += GetYPointDynamicDraw
    gp_y.Get()
    if gp_y.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    y_pt = gp_y.Point()

    # Create the final plane for the block operations
    plane = rs.PlaneFromPoints(origin, x_pt, y_pt)
    if( plane == None ):
        print("Invalid points selected for plane.")
        return 1

    # Prompt user with a dialog box for the block name
    block_name = rs.StringBox(message="Enter block name:", default_value="", title="Block Name")
    if( block_name == None ):
        return 1
        
    if rs.IsBlock(block_name):
        print("A block with this name already exists.")
        return 1

    # calculate transformation matrix from the custom plane to world XY
    xform_to_world = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
    
    # copy geometry and transform to world origin to define the block
    copied_objs = rs.CopyObjects(object_ids)
    rs.TransformObjects(copied_objs, xform_to_world, copy=False)
    rs.AddBlock(copied_objs, [0,0,0], block_name, delete_input=True)
    
    # insert the instance at world origin and map it back to the custom plane
    instance_id = rs.InsertBlock(block_name, [0,0,0])
    xform_to_plane = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    rs.TransformObject(instance_id, xform_to_plane, copy=False)
    
    # delete the original objects to complete the replacement
    rs.DeleteObjects(object_ids)

    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

if __name__ == "__main__":
    RunCommand(True)
