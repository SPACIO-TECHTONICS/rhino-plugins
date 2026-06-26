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
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore
import Rhino.Geometry as rg  # type: ignore
from assets import ui_numberform as nf
from assets import osm_utilities as osm
from assets import auth_helper

__commandname__ = "knOSM3d"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knOSM3d"):
        return auth_helper.get_cancel_result()

    form_values = nf.show_eto_form_with_titles("Extrude Buildings Toolbox", "Level Height")
    if not form_values:
        return Rhino.Commands.Result.Cancel
    
    try:
        ht = float(form_values.values()[0])
    except (ValueError, IndexError):
        ht = 3.0 # Default fallback

    layer_name = "URBAN3D::buildings"
    if not rs.IsLayer(layer_name):
        rs.AddLayer(layer_name)
    else:
        existing_objs = rs.ObjectsByLayer(layer_name)
        if existing_objs:
            res = rs.MessageBox("Do you want to delete the existing buildings on layer {0}?".format(layer_name), 1, "Extrude Buildings Toolbox")
            if res == 1: 
                rs.EnableRedraw(False)
                rs.DeleteObjects(existing_objs)
                rs.EnableRedraw(True)
            else:
                return Rhino.Commands.Result.Cancel
                
    rs.CurrentLayer(layer_name)
    
    source_layer = "URBAN2D::buildings"
    if not rs.IsLayer(source_layer):
        rs.MessageBox("Source layer {0} not found.".format(source_layer))
        return Rhino.Commands.Result.Failure

    bldg_crvs = rs.ObjectsByLayer(source_layer)
    if not bldg_crvs:
        print("No curves found on {0}.".format(source_layer))
        return Rhino.Commands.Result.Nothing

    rs.EnableRedraw(False)
    try:
        for crv in bldg_crvs:
            n_lvl_str = rs.GetUserText(crv, "building:levels")
            try:
                n_lvl = float(n_lvl_str) if n_lvl_str else 1.0
            except ValueError:
                n_lvl = 1.0
                
            crv_geom = rs.coercecurve(crv)
            if not crv_geom: continue
            
            vec = rg.Vector3d(0, 0, n_lvl * ht)
            ext = rg.Extrusion.CreateExtrusion(crv_geom, vec)
            if ext:
                brep = ext.ToBrep()
                capped = brep.CapPlanarHoles(sc.doc.ModelAbsoluteTolerance)
                if capped:
                    obj_id = sc.doc.Objects.AddBrep(capped)
                    osm.TransferObjUserText(crv, obj_id)

        rs.EnableRedraw(True)
        return Rhino.Commands.Result.Success
    except Exception as e:
        rs.EnableRedraw(True)
        print("Error extruding buildings: {0}".format(e))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
