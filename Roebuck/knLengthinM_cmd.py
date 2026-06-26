# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Calculates the total length of selected curves or edges in meters, scaling automatically from the active document unit system."""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

__commandname__ = "knLengthinM"

def calculate_length_in_meters(geos):
    doc_units = sc.doc.ModelUnitSystem
    target_units = Rhino.UnitSystem.Meters
    scale = Rhino.RhinoMath.UnitScale(doc_units, target_units)
    
    total_len = 0.0
    for geo in geos:
        if rs.IsCurve(geo):
            total_len += (rs.CurveLength(geo) * scale)
        else:
            curve = rs.coercecurve(geo)
            if curve:
                total_len += (curve.GetLength() * scale)
    return total_len

def RunCommand(is_interactive):


print("Executing " + __commandname__)

    geos = rs.GetObjects("Select curves/edges for length in Meters", 
                         rs.filter.curve | rs.filter.edgeobject, 
                         preselect=True)
    if not geos: return 1
    
    length = calculate_length_in_meters(geos)
    formatted = "{:,.2f}".format(length)
    
    print("Total Length = {} Meters".format(formatted))
    rs.ClipboardText(formatted.replace(",", ""))
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
