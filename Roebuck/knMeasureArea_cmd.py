# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Calculates the total area of selected geometries in a target unit system (SF, SM, SQMM, SQCM, or Acres) without changing the active document units."""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
import scriptcontext as sc

__commandname__ = "knMeasureArea"


def calculate_area_with_units(geos, target_unit_name="SF"):
    """
    Calculates total area of geometries in a target unit without changing doc units.
    """
    total_area = 0.0
    doc_unit_system = sc.doc.ModelUnitSystem

    unit_map = {
        "SF": Rhino.UnitSystem.Feet,
        "SM": Rhino.UnitSystem.Meters,
        "SQMM": Rhino.UnitSystem.Millimeters,
        "SQCM": Rhino.UnitSystem.Centimeters,
    }

    target_unit = unit_map.get(target_unit_name.upper(), doc_unit_system)

    scale = Rhino.RhinoMath.UnitScale(doc_unit_system, target_unit)
    area_factor = scale * scale

    if target_unit_name.upper() == "ACRE":
        scale_to_feet = Rhino.RhinoMath.UnitScale(
            doc_unit_system, Rhino.UnitSystem.Feet
        )
        area_factor = (scale_to_feet * scale_to_feet) / 43560.0

    for geo in geos:
        rhobj = rs.coercerhinoobject(geo, True, True)
        if rhobj:
            amp = rg.AreaMassProperties.Compute(rhobj.Geometry)
            if amp:
                total_area += amp.Area * area_factor
            else:
                if rs.IsCurve(geo) and rs.IsCurveClosed(geo) and rs.IsCurvePlanar(geo):
                    total_area += rs.CurveArea(geo)[0] * area_factor

    return total_area


def RunCommand(is_interactive):

    geos = rs.GetObjects(
        "Select geometries for area measurement",
        rs.filter.curve
        | rs.filter.surface
        | rs.filter.polysurface
        | rs.filter.mesh
        | rs.filter.extrusion,
        preselect=True,
    )
    if not geos:
        return 1

    units = ["SF", "SM", "ACRE", "SQMM", "SQCM", "Current"]
    target_unit = rs.ListBox(units, "Select target unit for conversion", "Measure Area")
    if not target_unit:
        return 1

    display_unit = target_unit
    if target_unit == "Current":
        display_unit = str(sc.doc.ModelUnitSystem)

    area = calculate_area_with_units(geos, target_unit)

    formatted_area = "{:,.2f}".format(area)
    result_str = "{} {}".format(formatted_area, display_unit)

    print("Total Area = ") + result_str
    rs.ClipboardText(formatted_area.replace(",", ""))

    return 0


if __name__ == "__main__":
    RunCommand(True)
