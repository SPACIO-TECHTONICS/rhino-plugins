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

"""Mirrors selected objects across a reference planar surface using the surface's midpoint tangent frame as the mirror plane."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore

__commandname__ = "knMirrorBySurface" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # Get objects to mirror
    objs = rs.GetObjects("Select objects to mirror", preselect=True)
    if not objs: 
        return 1

    # Get the reference surface
    srf = rs.GetObject("Select reference surface as mirror plane", rs.filter.surface | rs.filter.polysurface)
    if not srf: 
        return 1

    # Prompt to delete input objects
    del_str = rs.GetString("Delete input objects?", "No", ["Yes", "No"])
    if not del_str: 
        return 1
        
    delete_input = (del_str.lower() == "yes")
    copy_objs = not delete_input

    # Extract domain to find the center of the surface
    domainU = rs.SurfaceDomain(srf, 0)
    domainV = rs.SurfaceDomain(srf, 1)
    u = domainU[0] + (domainU[1] - domainU[0]) / 2.0
    v = domainV[0] + (domainV[1] - domainV[0]) / 2.0

    # Get the plane at the center of the surface
    plane = rs.SurfaceFrame(srf, [u, v])
    
    if plane:
        # Create mirror transform
        xform = Rhino.Geometry.Transform.Mirror(plane)
        
        # Apply transform (copy_objs determines if originals are kept or modified directly)
        new_objs = rs.TransformObjects(objs, xform, copy_objs)
        
        # If objects were copied (Delete = No), strip the inherited groups
        # If objects were NOT copied (Delete = Yes), Rhino automatically keeps them in their groups
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