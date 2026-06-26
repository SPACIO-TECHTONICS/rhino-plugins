# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
import scriptcontext as sc

__commandname__ = "knAreainSM"

def RunCommand( is_interactive ):


print("Executing " + __commandname__)

    geos = rs.GetObjects("Select Geometries to measure area in sq.m", 
                         rs.filter.curve | rs.filter.surface | rs.filter.polysurface | rs.filter.mesh | rs.filter.extrusion)
    if not geos: return

    doc_unit_system = sc.doc.ModelUnitSystem
    scale = Rhino.RhinoMath.UnitScale(doc_unit_system, Rhino.UnitSystem.Meters)
    area_factor = scale * scale
    
    areatotal = 0.0
    validobjs = 0
    invalidobjs = 0
    
    for geo in geos:
        rhobj = rs.coercerhinoobject(geo, True, True)
        if rhobj:
            amp = rg.AreaMassProperties.Compute(rhobj.Geometry)
            if amp:
                areatotal += (amp.Area * area_factor)
                validobjs += 1
            else:
                if rs.IsCurve(geo) and rs.IsCurveClosed(geo):
                    areatotal += (rs.CurveArea(geo)[0] * area_factor)
                    validobjs += 1
                else:
                    invalidobjs += 1
        else:
            invalidobjs += 1
            
    print("Area in sq.m = {:,.2f} sq.m").format(areatotal)
    print("Invalid objects = {}").format(invalidobjs) 
    print("Valid objects = {}").format(validobjs)
    
    rs.ClipboardText("{:.2f}".format(areatotal))
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
