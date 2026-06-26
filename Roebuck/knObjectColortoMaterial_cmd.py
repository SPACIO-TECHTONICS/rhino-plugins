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

"""Assigns the object's layer/display color as its render material color, and sets the print color to match."""

import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knObjectColortoMaterial"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


sourceObjects = rs.GetObjects(message="Select Objects to use color", preselect=True, select=False)
    
    for obj in sourceObjects:
        obj_color = rs.ObjectColor(obj)
        obj_mat = rs.ObjectMaterialIndex(obj)
        if obj_mat == -1:
            obj_mat = rs.AddMaterialToObject(obj)
        rs.MaterialColor(obj_mat, obj_color)
        rs.ObjectPrintColor(obj, color=rs.ObjectColor(obj))

if __name__ == "__main__":
    RunCommand(True)
