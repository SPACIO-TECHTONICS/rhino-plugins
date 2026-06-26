# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Orients multiple planar surfaces or curves to the World XY plane using a change-of-basis transformation."""

import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knOrienttoCPlane"

def RunCommand(is_interactive):
    # Select multiple objects
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
                # Corrected: Use SurfaceFrame to get the plane of a surface
                # Parameter [0,0] gets the frame at the start of the surface UV
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
            # Change-of-Basis transformation
            xform = rs.XformChangeBasis(target_plane, plane)
            rs.TransformObject(obj_id, xform)
            success_count += 1

    print "Successfully oriented {0} objects.".format(success_count)
    if error_count > 0:
        print "{0} objects were skipped (non-planar).".format(error_count)
    
    return 0

if __name__ == "__main__":
    RunCommand(True)