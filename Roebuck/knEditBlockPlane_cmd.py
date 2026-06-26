# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System.Drawing.Color as Color

__commandname__ = "knEditBlockPlane"

def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    instance_id = rs.GetObject("Select a block instance to edit its reference plane", rs.filter.instance)
    if( instance_id == None ):
        return 1
        
    block_name = rs.BlockInstanceName(instance_id)
    instance_xform = rs.BlockInstanceXform(instance_id)
    
    gp_origin = Rhino.Input.Custom.GetPoint()
    gp_origin.SetCommandPrompt("Select NEW reference plane origin (base point)")
    gp_origin.Get()
    if gp_origin.CommandResult() != Rhino.Commands.Result.Success:
        return 1
    origin = gp_origin.Point()
        
    gp_x = Rhino.Input.Custom.GetPoint()
    gp_x.SetCommandPrompt("Select a point on the NEW reference plane's X-axis")
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

    rc, inv_xform = instance_xform.TryGetInverse()
    if not rc: 
        print("Failed to invert instance transform.")
        return 1
        
    local_plane = world_plane.Clone()
    local_plane.Transform(inv_xform)

    xform_def = Rhino.Geometry.Transform.ChangeBasis(Rhino.Geometry.Plane.WorldXY, local_plane)
    xform_inst_offset = Rhino.Geometry.Transform.ChangeBasis(local_plane, Rhino.Geometry.Plane.WorldXY)

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
    
    instances = idef.GetReferences(1) 
    for inst in instances:
        old_xform = inst.InstanceXform
        new_xform = old_xform * xform_inst_offset
        rc, inv_old = old_xform.TryGetInverse()
        if rc:
            delta_xform = new_xform * inv_old
            rs.TransformObject(inst.Id, delta_xform, copy=False)

    sc.doc.Views.Redraw()

    return 0

if __name__ == "__main__":
    RunCommand(True)
