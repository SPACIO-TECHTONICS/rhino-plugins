# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Aligns the active viewport camera and construction plane (CPlane) to the normal of a selected surface face at the clicked location."""

import rhinoscriptsyntax as rs

__commandname__ = "knAlignViewtoSrf"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    srf_info = rs.GetSurfaceObject("Select a surface to create CPlane and align view")
    if( srf_info != None ):
        srf_id = srf_info[0]
        pt = srf_info[3]
        
        uv = rs.SurfaceClosestPoint(srf_id, pt)
        if( uv != None ):
            plane = rs.SurfaceFrame(srf_id, uv)
            if( plane != None ):
                
                views = rs.ViewNames()
                target_view = None
                for view in views:
                    if view.lower() not in ["top", "perspective"]:
                        target_view = view
                        break
                        
                if target_view != None:
                    rs.CurrentView(target_view)
                    
                    rs.ViewCPlane(target_view, plane)
                    rs.Command("-_Plan _Enter", False)
                else:
                    print "Could not find a suitable viewport. Please ensure Front, Right, or similar views are open."

    return 0

RunCommand(True)