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

import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
from assets import auth_helper

__commandname__ = "knProjectSrftoTerrain"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knProjectSrftoTerrain"):
        return auth_helper.get_cancel_result()

    srfs = rs.GetObjects(message="Select surfaces to project", filter=8, preselect=True)
    if not srfs:
        return Rhino.Commands.Result.Cancel
        
    terrain = rs.GetObject("Select the terrain to project onto", 8 | 16 | 32)
    if not terrain:
        return Rhino.Commands.Result.Cancel

    rs.EnableRedraw(False)
    temp_objs = []
    final_crvs = []
    
    try:
        is_mesh = rs.IsMesh(terrain)
        if is_mesh:
            target_brep = rs.MeshToNurb(terrain)
            temp_objs.append(target_brep)
        else:
            target_brep = terrain

        for srf in srfs:
            border = rs.DuplicateSurfaceBorder(srf)
            if not border: continue
            
            for b_crv in border:
                rs.EnableObjectGrips(b_crv)
                grips = rs.ObjectGripLocations(b_crv)
                
                projected_grips = []
                for pt in grips:
                    z_up = rs.ShootRay(target_brep, pt, (0, 0, 1), 1)
                    z_down = rs.ShootRay(target_brep, pt, (0, 0, -1), 1)
                    
                    if z_up:
                        projected_grips.append(z_up[1])
                    elif z_down:
                        projected_grips.append(z_down[1])
                    else:
                        cp = rs.BrepClosestPoint(target_brep, pt)
                        if cp:
                            projected_grips.append(cp[0])
                        else:
                            projected_grips.append(pt)
                
                rs.ObjectGripLocations(b_crv, projected_grips)
                rs.EnableObjectGrips(b_crv, False)
                final_crvs.append(b_crv)
        
        if final_crvs:
            rs.SelectObjects(final_crvs)
            rs.Command("-_Patch Enter", False)
            rs.DeleteObjects(final_crvs)
        
        if is_mesh and temp_objs:
            rs.DeleteObjects(temp_objs)
            
        rs.EnableRedraw(True)
        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        if final_crvs: rs.DeleteObjects(final_crvs)
        if is_mesh and temp_objs: rs.DeleteObjects(temp_objs)
        print("Error projecting surfaces: {0}".format(e))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
