# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs

__commandname__ = "knCircleOnSrf"

def RunCommand( is_interactive ):
    print "Running", __commandname__
    
    srf_id = rs.GetSurfaceObject("Select surface for circle placement", preselect=True)
    if not srf_id:
        return 1
        
    surface = srf_id[0]
    
    point = rs.GetPointOnSurface(surface, "Pick circle center point on surface")
    if point is None:
        return 1
        
    radius = rs.GetReal("Circle radius", 1.0, minimum=0.0)
    if radius is None:
        return 1
        
    uv = rs.SurfaceClosestPoint(surface, point)
    
    normal = rs.SurfaceNormal(surface, uv)
    
    if normal:
        plane = rs.PlaneFromNormal(point, normal)
        rs.AddCircle(plane, radius)
        return 0
        
    return 1

RunCommand(True)