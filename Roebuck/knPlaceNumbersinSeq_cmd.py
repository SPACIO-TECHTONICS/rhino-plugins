# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Places text numbers sequentially at user-selected points in the active Rhino viewport."""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import Rhino

def RunCommand( is_interactive ):


print("Executing"), __commandname__ targeting the active Rhino document
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    
    pts = rs.GetPoints(True, False, "Select Locations", "Select Next Location")
    
    if not pts: return
    
    count = 1
    for pt in pts:
        plane = rg.Plane.WorldXY
        plane.Origin = pt
        
        text_height = 1.0 
        text_str = str(count)
        
        text_entity = rg.TextEntity.Create(
            text_str, 
            plane, 
            sc.doc.DimStyles.Current, 
            False, 
            0, 
            0
        )
        
        sc.doc.Objects.AddText(text_entity)
        
        count += 1
    
    sc.doc.Views.Redraw()

if __name__ == "__main__":
    RunCommand(True)
