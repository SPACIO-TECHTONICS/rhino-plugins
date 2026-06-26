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
from assets import auth_helper

__commandname__ = "knMassFloorArea"

def _calc_projected_area(mesh, tolerance):
    """Helper function to calculate the projected area of a single mesh."""
    if not mesh.IsValid or mesh.Faces.Count == 0:
        return 0.0

    plane = Rhino.Geometry.Plane.WorldXY
    outlines = mesh.GetOutlines(plane)

    if not outlines:
        return 0.0

    curves = [poly.ToNurbsCurve() for poly in outlines if poly.IsValid]

    if not curves:
        return 0.0

    planar_breps = Rhino.Geometry.Brep.CreatePlanarBreps(curves, tolerance)
    area = 0.0

    if planar_breps:
        for b in planar_breps:
            amp = Rhino.Geometry.AreaMassProperties.Compute(b)
            if amp:
                area += amp.Area
    else:
        for crv in curves:
            if crv.IsClosed:
                amp = Rhino.Geometry.AreaMassProperties.Compute(crv)
                if amp:
                    area += amp.Area
                    
    return area


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knMassFloorArea"):
        return auth_helper.get_cancel_result()

    # 1. Prompt user to select masses
    obj_ids = rs.GetObjects("Select masses (Polysurfaces or Meshes)", rs.filter.polysurface | rs.filter.surface | rs.filter.mesh)
    if not obj_ids:
        return Rhino.Commands.Result.Cancel

    # 2. Ask for calculation method if multiple objects are selected
    calc_method = "Footprint"
    if len(obj_ids) > 1:
        options = ["Footprint", "SumOfIndividuals"]
        result = rs.GetString("Multiple objects selected. Calculate combined footprint or sum of individual areas?", "Footprint", options)
        if not result or result not in options:
            return Rhino.Commands.Result.Cancel
        calc_method = result

    tolerance = sc.doc.ModelAbsoluteTolerance
    total_area = 0.0

    # 3. Process geometry based on user choice
    if calc_method == "Footprint":
        combined_mesh = Rhino.Geometry.Mesh()
        for obj_id in obj_ids:
            geo = rs.coercegeometry(obj_id)
            if isinstance(geo, Rhino.Geometry.Brep):
                mp = Rhino.Geometry.MeshingParameters.Default
                meshes = Rhino.Geometry.Mesh.CreateFromBrep(geo, mp)
                if meshes:
                    for m in meshes:
                        combined_mesh.Append(m)
            elif isinstance(geo, Rhino.Geometry.Mesh):
                combined_mesh.Append(geo)
                
        total_area = _calc_projected_area(combined_mesh, tolerance)

    else:
        for obj_id in obj_ids:
            single_mesh = Rhino.Geometry.Mesh()
            geo = rs.coercegeometry(obj_id)
            if isinstance(geo, Rhino.Geometry.Brep):
                mp = Rhino.Geometry.MeshingParameters.Default
                meshes = Rhino.Geometry.Mesh.CreateFromBrep(geo, mp)
                if meshes:
                    for m in meshes:
                        single_mesh.Append(m)
            elif isinstance(geo, Rhino.Geometry.Mesh):
                single_mesh.Append(geo)
                
            total_area += _calc_projected_area(single_mesh, tolerance)

    # 4. Map document units to standard area abbreviations
    unit_system = sc.doc.ModelUnitSystem
    unit_map = {
        Rhino.UnitSystem.Millimeters: "sq.mm",
        Rhino.UnitSystem.Centimeters: "sq.cm",
        Rhino.UnitSystem.Meters: "sq.m",
        Rhino.UnitSystem.Inches: "sq.in",
        Rhino.UnitSystem.Feet: "sf",
        Rhino.UnitSystem.Yards: "sq.yd",
        Rhino.UnitSystem.Miles: "sq.mi",
        Rhino.UnitSystem.Kilometers: "sq.km"
    }
    
    sq_unit_str = unit_map.get(unit_system, "sq.{0}".format(str(unit_system).lower()))

    # 5. Format output, print it, and copy to clipboard
    output_str = "{0} {1}".format(total_area, sq_unit_str)
    
    print(output_str)
    rs.ClipboardText(output_str)

    return Rhino.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
