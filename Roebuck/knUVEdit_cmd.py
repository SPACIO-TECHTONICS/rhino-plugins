# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import rhinoscriptsyntax as rs

__commandname__ = "knUVEdit"

def RunCommand( is_interactive ):


    print("Executing", __commandname__)
    
    mesh_id = rs.GetObject("Select a mesh to edit its UVs", rs.filter.mesh)
    if not mesh_id: 
        return 1
        
    uvs = rs.MeshTextureCoordinates(mesh_id)
    if not uvs:
        print("This mesh does not have existing texture coordinates.")
        return 1
        
    pt1 = rs.GetPoint("Click starting point for UV shift")
    if pt1 is None: 
        return 1
        
    pt2 = rs.GetPoint("Click target point", pt1)
    if pt2 is None: 
        return 1
        
    delta = pt2 - pt1
    uv_scale = 0.01 
    
    new_uvs = []
    for uv in uvs:
        new_uvs.append([uv.X + (delta.X * uv_scale), uv.Y + (delta.Y * uv_scale)])
        
    rs.MeshTextureCoordinates(mesh_id, new_uvs)
    print("UVs Shifted successfully.")
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
