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
import Rhino  # type: ignore
from assets import auth_helper

__commandname__ = "knShowPrograms"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knShowPrograms"):
        return auth_helper.get_cancel_result()

    all_objects = rs.AllObjects()
    if not all_objects:
        print("No objects found in the document.")
        return Rhino.Commands.Result.Nothing

    temp_layer = "Temp_Name_Dots"
    if not rs.IsLayer(temp_layer):
        rs.AddLayer(temp_layer, color=(255, 150, 0)) 
        
    created_dots = []
    rs.EnableRedraw(False)
    
    try:
        for obj in all_objects:
            name = rs.ObjectName(obj)
            if name:
                bbox = rs.BoundingBox(obj)
                if bbox:
                    center_pt = (bbox[0] + bbox[6]) / 2.0
                    dot_id = rs.AddTextDot(name, center_pt)
                    rs.ObjectLayer(dot_id, temp_layer)
                    created_dots.append(dot_id)
                    
        rs.EnableRedraw(True)
        
        if not created_dots:
            print("No named objects were found.")
            if rs.IsLayerEmpty(temp_layer):
                rs.DeleteLayer(temp_layer)
            return Rhino.Commands.Result.Nothing

        rs.GetString("Showing {0} names. Press Enter, Space, or type any key to delete them...".format(len(created_dots)))
        
        rs.EnableRedraw(False)
        if created_dots:
            rs.DeleteObjects(created_dots)
        
        if rs.IsLayerEmpty(temp_layer):
            rs.DeleteLayer(temp_layer)
            
        rs.EnableRedraw(True)
        print("Temporary dots deleted.")
        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error showing programs: {0}".format(e))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)

if __name__ == "__main__":
    RunCommand(True)
