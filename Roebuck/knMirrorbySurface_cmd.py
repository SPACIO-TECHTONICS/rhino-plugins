# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Mirrors selected objects across a reference planar surface using the surface's midpoint tangent frame as the mirror plane."""

import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "knMirrorBySurface"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    objs = rs.GetObjects("Select objects to mirror", preselect=True)
    if not objs: 
        return 1

    srf = rs.GetObject("Select reference surface as mirror plane", rs.filter.surface | rs.filter.polysurface)
    if not srf: 
        return 1

    del_str = rs.GetString("Delete input objects?", "No", ["Yes", "No"])
    if not del_str: 
        return 1
        
    delete_input = (del_str.lower() == "yes")
    copy_objs = not delete_input

    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[0] + (domainU[1] - domainU[0]) / 2.0
    v = domainV[0] + (domainV[1] - domainV[0]) / 2.0

    plane = rs.SurfaceFrame(srf, [u, v])
    
    if plane:
        xform = Rhino.Geometry.Transform.Mirror(plane)
        
        new_objs = rs.TransformObjects(objs, xform, copy_objs)
        
        if copy_objs and new_objs:
            for obj in new_objs:
                inherited_groups = rs.ObjectGroups(obj)
                if inherited_groups:
                    for group in inherited_groups:
                        rs.RemoveObjectFromGroup(obj, group)
                        
        return 0
    else:
        print "Could not determine a plane from the selected surface."
        return 1

RunCommand(True)