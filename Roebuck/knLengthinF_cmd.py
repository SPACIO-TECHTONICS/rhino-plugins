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

"""Calculates the total length of selected curves or edges in feet, scaling automatically from the active document unit system."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knLengthinF"

def calculate_length_in_feet(geos):
    doc_units = sc.doc.ModelUnitSystem
    target_units = Rhino.UnitSystem.Feet
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
    geos = rs.GetObjects("Select curves/edges for length in Feet", 
                         rs.filter.curve | rs.filter.edgeobject, 
                         preselect=True)
    if not geos: return 1
    
    length = calculate_length_in_feet(geos)
    formatted = "{:,.2f}".format(length)
    
    print("Total Length = {} Feet".format(formatted))
    rs.ClipboardText(formatted.replace(",", ""))
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
