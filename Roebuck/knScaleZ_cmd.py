# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Scales selected objects dynamically and exclusively along the Z-axis, with real-time preview and snapping capabilities."""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System

__commandname__ = "knScaleZ"

class InteractiveZScale(Rhino.Input.Custom.GetTransform):
    def __init__(self, base_pt, ref_pt):
        Rhino.Input.Custom.GetTransform.__init__(self)
        
        self.base_pt = base_pt
        self.ref_pt = ref_pt
        
        self.dz0 = ref_pt.Z - base_pt.Z
        
        if abs(self.dz0) < 1e-8:
            self.dz0 = 1e-8

    def CalculateTransform(self, viewport, point):
        dz1 = point.Z - self.base_pt.Z
        factor = dz1 / self.dz0
        
        plane = Rhino.Geometry.Plane(self.base_pt, Rhino.Geometry.Vector3d.ZAxis)
        
        xform = Rhino.Geometry.Transform.Scale(plane, 1.0, 1.0, factor)
        return xform
        
    def OnDynamicDraw(self, e):
        e.Display.DrawDottedLine(self.base_pt, self.ref_pt, System.Drawing.Color.DarkGray)
        Rhino.Input.Custom.GetTransform.OnDynamicDraw(self, e)

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    objects = rs.GetObjects("Select objects to dynamically scale in Z-axis", preselect=True)
    if not objects: return 1
    
    base_pt = rs.GetPoint("Origin point")
    if not base_pt: return 1
    
    ref_pt = rs.GetPoint("Reference point for first scale factor", base_pt)
    if not ref_pt: return 1
    
    tracker = InteractiveZScale(base_pt, ref_pt)
    
    xform_list = Rhino.Collections.TransformObjectList()
    
    for obj_id in objects:
        rhino_obj = sc.doc.Objects.Find(obj_id)
        if rhino_obj:
            xform_list.Add(rhino_obj)
            
    tracker.AddTransformObjects(xform_list)
            
    tracker.SetCommandPrompt("Target point (snapping will only use Z-elevation)")
    tracker.SetBasePoint(base_pt, True) 
    
    tracker.Get()
    
    if tracker.CommandResult() != Rhino.Commands.Result.Success:
        return 1
        
    final_xform = tracker.CalculateTransform(tracker.View().ActiveViewport, tracker.Point())
    
    for obj_id in objects:
        sc.doc.Objects.Transform(obj_id, final_xform, True)
        
    sc.doc.Views.Redraw()
    return 0

RunCommand(True)