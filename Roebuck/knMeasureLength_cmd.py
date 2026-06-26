# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Calculates the total length of selected curves or edges in a target unit system (Feet, Meters, Millimeters, Centimeters, or Inches) without changing the active document units."""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

__commandname__ = "knMeasureLength"


def calculate_length_with_units(geos, target_unit_name="F"):
    """
    Calculates total length of geometries in a target unit without changing doc units.
    """
    total_len = 0.0
    doc_unit_system = sc.doc.ModelUnitSystem

    unit_map = {
        "F": Rhino.UnitSystem.Feet,
        "M": Rhino.UnitSystem.Meters,
        "MM": Rhino.UnitSystem.Millimeters,
        "CM": Rhino.UnitSystem.Centimeters,
        "IN": Rhino.UnitSystem.Inches,
    }

    target_unit = unit_map.get(target_unit_name.upper(), doc_unit_system)

    scale = Rhino.RhinoMath.UnitScale(doc_unit_system, target_unit)

    for geo in geos:
        if rs.IsCurve(geo):
            total_len += rs.CurveLength(geo) * scale
        else:
            curve = rs.coercecurve(geo)
            if curve:
                total_len += curve.GetLength() * scale

    return total_len


def RunCommand(is_interactive):

    geos = rs.GetObjects(
        "Select curves or edges for length measurement",
        rs.filter.curve | rs.filter.edgeobject,
        preselect=True,
    )
    if not geos:
        return 1

    units = ["F", "M", "MM", "CM", "IN", "Current"]
    target_unit = rs.ListBox(
        units, "Select target unit for conversion", "Measure Length"
    )
    if not target_unit:
        return 1

    display_unit = target_unit
    if target_unit == "Current":
        display_unit = str(sc.doc.ModelUnitSystem)

    length = calculate_length_with_units(geos, target_unit)

    formatted_len = "{:,.2f}".format(length)
    result_str = "{} {}".format(formatted_len, display_unit)
    print("Total Length = " + result_str)
    rs.ClipboardText(formatted_len.replace(",", ""))

    return 0


if __name__ == "__main__":
    RunCommand(True)
