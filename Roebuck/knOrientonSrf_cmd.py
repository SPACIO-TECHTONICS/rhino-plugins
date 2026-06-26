# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Orients a selected block instance onto a planar surface, with options to align using the block's native reference plane or a flat World Z-normal plane."""

import rhinoscriptsyntax as rs
import Rhino

__commandname__ = "knOrientonSrf"

def RunCommand( is_interactive ):


print("Executing"), __commandname__
    
    block_id = rs.GetObject("Select a block instance to orient", rs.filter.instance)
    if block_id is None: 
        return 1
        
    use_ref = rs.GetString("Use the block's reference plane as the source plane?", "Yes", ["Yes", "No"])
    if use_ref is None:
        return 1
        
    srf_id = rs.GetObject("Select a planar surface", rs.filter.surface)
    if srf_id is None: 
        return 1
        
    if not rs.IsSurfacePlanar(srf_id):
        print("The selected surface is not planar.")
        return 1
        
    u_domain = rs.SurfaceDomain(srf_id, 0)
    v_domain = rs.SurfaceDomain(srf_id, 1)
    u_mid = u_domain[0] + (u_domain[1] - u_domain[0]) / 2.0
    v_mid = v_domain[0] + (v_domain[1] - v_domain[0]) / 2.0
    
    target_plane = rs.SurfaceFrame(srf_id, [u_mid, v_mid])
    
    insert_pt = rs.BlockInstanceInsertPoint(block_id)
    
    if use_ref.lower() == "yes":
        xform_block = rs.BlockInstanceXform(block_id)
        
        pt_origin = rs.PointTransform([0,0,0], xform_block)
        pt_x = rs.PointTransform([1,0,0], xform_block)
        pt_y = rs.PointTransform([0,1,0], xform_block)
        
        vec_x = rs.VectorCreate(pt_x, pt_origin)
        vec_y = rs.VectorCreate(pt_y, pt_origin)
        
        source_plane = rs.PlaneFromFrame(pt_origin, vec_x, vec_y)
    else:
        source_plane = rs.PlaneFromNormal(insert_pt, [0, 0, 1])
    
    xform_orient = Rhino.Geometry.Transform.PlaneToPlane(source_plane, target_plane)
    
    rs.TransformObject(block_id, xform_orient, copy=True)
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
