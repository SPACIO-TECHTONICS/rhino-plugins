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
