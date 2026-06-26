"""Calculates the total length of selected curves or edges in a target unit system (Feet, Meters, Millimeters, Centimeters, or Inches) without changing the active document units."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knMeasureLength"

def calculate_length_with_units(geos, target_unit_name="F"):
    """
    Calculates total length of geometries in a target unit without changing doc units.
    """
    total_len = 0.0
    doc_unit_system = sc.doc.ModelUnitSystem
    
    # Map friendly names to Rhino unit systems
    unit_map = {
        "F": Rhino.UnitSystem.Feet,
        "M": Rhino.UnitSystem.Meters,
        "MM": Rhino.UnitSystem.Millimeters,
        "CM": Rhino.UnitSystem.Centimeters,
        "IN": Rhino.UnitSystem.Inches,
    }
    
    target_unit = unit_map.get(target_unit_name.upper(), doc_unit_system)
    
    # Calculate scale factor from doc units to target units
    scale = Rhino.RhinoMath.UnitScale(doc_unit_system, target_unit)
    
    for geo in geos:
        # Check if it's a curve or a reference to an edge
        if rs.IsCurve(geo):
            total_len += (rs.CurveLength(geo) * scale)
        else:
            # Try to coerce to a curve (works for SubD edges, etc.)
            curve = rs.coercecurve(geo)
            if curve:
                total_len += (curve.GetLength() * scale)
                
    return total_len

def RunCommand(is_interactive):


# Prompt for curves or edges
    geos = rs.GetObjects("Select curves or edges for length measurement", 
                         rs.filter.curve | rs.filter.edgeobject, 
                         preselect=True)
    if not geos: return 1
    
    # Unit options
    units = ["F", "M", "MM", "CM", "IN", "Current"]
    target_unit = rs.ListBox(units, "Select target unit for conversion", "Measure Length")
    if not target_unit: return 1
    
    display_unit = target_unit
    if target_unit == "Current":
        display_unit = str(sc.doc.ModelUnitSystem)
    
    length = calculate_length_with_units(geos, target_unit)
    
    # Format result (2 decimal places)
    formatted_len = "{:,.2f}".format(length)
    result_str = "{} {}".format(formatted_len, display_unit)
    print("Total Length = " + result_str)
    rs.ClipboardText(formatted_len.replace(",", "")) # Raw number for clipboard
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
