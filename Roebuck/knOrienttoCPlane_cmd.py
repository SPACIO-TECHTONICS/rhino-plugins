# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Orients multiple planar surfaces or curves to the World XY plane using a change-of-basis transformation."""

import rhinoscriptsyntax as rs

__commandname__ = "knOrienttoCPlane"

def RunCommand(is_interactive):
    obj_ids = rs.GetObjects("Select planar surfaces or curves to orient to World XY", 
                            rs.filter.surface | rs.filter.curve)
    
    if not obj_ids:
        return 1

    target_plane = rs.WorldXYPlane()
    success_count = 0
    error_count = 0

    for obj_id in obj_ids:
        plane = None
        
        if rs.IsSurface(obj_id):
            if rs.IsSurfacePlanar(obj_id):
                domain_u = rs.SurfaceDomain(obj_id, 0)
                domain_v = rs.SurfaceDomain(obj_id, 1)
                plane = rs.SurfaceFrame(obj_id, [domain_u[0], domain_v[0]])
            else:
                error_count += 1
                continue
        
        elif rs.IsCurve(obj_id):
            if rs.IsCurvePlanar(obj_id):
                plane = rs.CurvePlane(obj_id)
            else:
                error_count += 1
                continue

        if plane:
            xform = rs.XformChangeBasis(target_plane, plane)
            rs.TransformObject(obj_id, xform)
            success_count += 1

    print "Successfully oriented {0} objects.".format(success_count)
    if error_count > 0:
        print "{0} objects were skipped (non-planar).".format(error_count)
    
    return 0

if __name__ == "__main__":
    RunCommand(True)