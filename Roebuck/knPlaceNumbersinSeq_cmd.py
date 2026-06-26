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

"""Places text numbers sequentially at user-selected points in the active Rhino viewport."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino.Geometry as rg  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore

def RunCommand( is_interactive ):


print("Executing"), __commandname__ targeting the active Rhino document
    # Ensure we are targeting the active Rhino document
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    
    pts = rs.GetPoints(True, False, "Select Locations", "Select Next Location")
    
    if not pts: return # Safety check if user cancels
    
    count = 1
    for pt in pts:
        # 1. Define the plane (World XY shifted to point)
        plane = rg.Plane.WorldXY
        plane.Origin = pt
        
        # 2. Create the TextEntity (Geometry in memory)
        # Using 1.0 as a default height if DimStyle is unclear
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
        
        # 3. ADD TO DOCUMENT (This makes it visible)
        sc.doc.Objects.AddText(text_entity)
        
        count += 1
    
    # 4. Redraw the views to show the new objects immediately
    sc.doc.Views.Redraw()

if __name__ == "__main__":
    RunCommand(True)
