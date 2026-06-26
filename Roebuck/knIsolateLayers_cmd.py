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

# Isolate Layers
# ver 1.01
# 

import rhinoscript.userinterface
import rhinoscript.geometry
import rhinoscriptsyntax as rs  # type: ignore
import Rhino as r  # type: ignore

__commandname__ = "knIsolateLayers"

def RunCommand( is_interactive ):


#Select Objects
    objs=rs.GetObjects("Select the objects",preselect=True)
    rs.UnselectAllObjects()
    if not objs: return r.Commands.Result.Failure
    rs.EnableRedraw(False)
    
    #Select all objects on the selected objects' layers
    layers=[rs.ObjectLayer(obj) for obj in objs]
    for layer in layers:
        ObjstoShow = rs.ObjectsByLayer(layer,True)
        rs.SelectObjects(ObjstoShow)

    #Invert Selection
    invobjs = rs.InvertSelectedObjects()
    
    #Hide Inverted Objects
    rs.HideObjects(invobjs)
    rs.EnableRedraw(True)
    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
