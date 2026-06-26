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

"""Orients a planar surface or curve along a path curve, aligning the object's planar frame tangent to the curve's direction."""

import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knOrientonCurve"

# RunCommand is called when the user enters the command name in Rhino.
# The command name is defined by the filename minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing"), __commandname__
    
    # 1. Select the object to orient (Surface or Curve)
    obj = rs.GetObject("Select planar surface or curve to orient", rs.filter.surface | rs.filter.curve)
    if not obj: return 1
    
    # 2. Get the source plane of the object
    source_plane = None
    
    if rs.IsSurface(obj) and rs.IsSurfacePlanar(obj):
        # Extract the frame at the center of the surface's UV domain
        domain_u = rs.SurfaceDomain(obj, 0)
        domain_v = rs.SurfaceDomain(obj, 1)
        u_center = (domain_u[0] + domain_u[1]) / 2.0
        v_center = (domain_v[0] + domain_v[1]) / 2.0
        source_plane = rs.SurfaceFrame(obj, [u_center, v_center])
        
    elif rs.IsCurve(obj) and rs.IsCurvePlanar(obj):
        source_plane = rs.CurvePlane(obj)
        
    else:
        print("Object is not planar. Orientation might be unpredictable.")
        # Fallback to WorldXY at the object's bounding box center if not planar
        bbox = rs.BoundingBox(obj)
        if bbox:
            center = (bbox[0] + bbox[6]) / 2.0
            source_plane = rs.PlaneFromNormal(center, [0,0,1])

    if not source_plane:
        print("Could not determine source plane.")
        return 1

    # 3. Select the target curve (the path)
    target_crv = rs.GetObject("Select curve to orient perpendicular to", rs.filter.curve)
    if not target_crv: return 1
    
    # 4. Pick point on the curve to define the perpendicular plane
    point_on_crv = rs.GetPointOnCurve(target_crv, "Pick point on curve for orientation")
    if not point_on_crv: return 1
    
    # 5. Calculate the perpendicular plane at that parameter
    param = rs.CurveClosestPoint(target_crv, point_on_crv)
    target_plane = rs.CurvePerpFrame(target_crv, param)
    
    if target_plane:
        # CONVERSION: Turn planes into 3-point lists (Origin, X-direction, Y-direction)
        ref_pts = [source_plane.Origin, source_plane.PointAt(1,0), source_plane.PointAt(0,1)]
        tar_pts = [target_plane.Origin, target_plane.PointAt(1,0), target_plane.PointAt(0,1)]
        
        # 6. Perform the orientation (flags=0 means MOVE. flags=1 means COPY)
        rs.OrientObject(obj, ref_pts, tar_pts, flags=0)
        
    # Return values: 0 == success, 1 == cancel
    return 0

if __name__ == "__main__":
    RunCommand(True)
