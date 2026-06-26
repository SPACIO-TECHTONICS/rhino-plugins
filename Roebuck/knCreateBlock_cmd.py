# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
import System.Drawing.Color as Color

__commandname__ = "knCreateBlock" 

def RunCommand( is_interactive ):


    print("Executing " + __commandname__)
    
    object_ids = rs.GetObjects("Select objects to define block", preselect=True)
    if( object_ids == None ):
        return 1

    gp_origin = Rhino.Input.Custom.GetPoint()
    gp_origin.SetCommandPrompt("Select reference plane origin (base point)")
    gp_origin.Get()
    if gp_origin.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    origin = gp_origin.Point()
        
    gp_x = Rhino.Input.Custom.GetPoint()
    gp_x.SetCommandPrompt("Select a point on the reference plane's X-axis")
    gp_x.SetBasePoint(origin, True)
    gp_x.DrawLineFromPoint(origin, True)
    gp_x.Get()
    if gp_x.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    x_pt = gp_x.Point()

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

    gp_y = Rhino.Input.Custom.GetPoint()
    gp_y.SetCommandPrompt("Select a point on the reference plane's Y-axis")
    gp_y.SetBasePoint(origin, True)
    gp_y.DynamicDraw += GetYPointDynamicDraw
    gp_y.Get()
    if gp_y.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    y_pt = gp_y.Point()

    plane = rs.PlaneFromPoints(origin, x_pt, y_pt)
    if( plane == None ):
        print("Invalid points selected for plane.")
        return 1

    block_name = rs.StringBox(message="Enter block name:", default_value="", title="Block Name")
    if( block_name == None ):
        return 1
        
    if rs.IsBlock(block_name):
        print("A block with this name already exists.")
        return 1

    xform_to_world = rs.XformChangeBasis(rs.WorldXYPlane(), plane)
    
    copied_objs = rs.CopyObjects(object_ids)
    rs.TransformObjects(copied_objs, xform_to_world, copy=False)
    rs.AddBlock(copied_objs, [0,0,0], block_name, delete_input=True)
    
    instance_id = rs.InsertBlock(block_name, [0,0,0])
    xform_to_plane = rs.XformChangeBasis(plane, rs.WorldXYPlane())
    rs.TransformObject(instance_id, xform_to_plane, copy=False)
    
    rs.DeleteObjects(object_ids)

    return 0

if __name__ == "__main__":
    RunCommand(True)
