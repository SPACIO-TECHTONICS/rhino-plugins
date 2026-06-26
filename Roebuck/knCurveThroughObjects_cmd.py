# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Draws an interpolated curve directly through the bottom-center or top-center bounding box points of selected objects in their exact selection order."""

import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "knCurveThroughObjects"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    objects = rs.GetObjects("Select objects in the exact order you want the curve to flow", preselect=True)
    if not objects: return 1
    
    if len(objects) < 2:
        print "You must select at least two objects to draw a curve."
        return 1
        
    default_align = "BottomCenter"
    if sc.sticky.has_key("knCurveThroughObjects_LastAlign"):
        default_align = sc.sticky["knCurveThroughObjects_LastAlign"]
        
    alignment = rs.GetString("Curve path alignment", default_align, ["BottomCenter", "TopCenter"])
    if not alignment: return 1
    
    sc.sticky["knCurveThroughObjects_LastAlign"] = alignment
        
    rs.EnableRedraw(False)
    points = []
    
    for obj in objects:
        bbox = rs.BoundingBox(obj)
        if not bbox: continue
        
        center_x = (bbox[0].X + bbox[2].X) / 2.0
        center_y = (bbox[0].Y + bbox[2].Y) / 2.0
        
        if alignment.lower() == "topcenter":
            target_z = bbox[4].Z
        else:
            target_z = bbox[0].Z
        
        base_pt = [center_x, center_y, target_z]
        points.append(base_pt)
        
    if len(points) >= 2:
        curve = rs.AddInterpCurve(points)
        
        if curve:
            rs.SelectObject(curve)
            print "Successfully generated {} interpolated curve through {} object centers.".format(alignment, len(points))
        else:
            print "Failed to generate curve."
    else:
        print "Not enough valid object bounding boxes found."
        
    rs.EnableRedraw(True)
    
    return 0

RunCommand(True)