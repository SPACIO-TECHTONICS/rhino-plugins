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

# Hide Layers
# ver 1.00
# 

import Rhino as r  # type: ignore
import rhinoscript.userinterface
import rhinoscript.geometry
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knHideLayers"


def RunCommand( is_interactive ):


#Select objects
  objs=rs.GetObjects("Select objects",preselect=True)
  
  if not objs: return r.Commands.Result.Failure
  rs.EnableRedraw(False)
  
  #Identify all layer of selection objects
  layers=[rs.ObjectLayer(obj) for obj in objs]
  
  #Hide objects on those layers
  for layer in layers: 
    ObjstoHide = rs.ObjectsByLayer(layer,True)
    rs.HideObjects(ObjstoHide)
  
  rs.EnableRedraw(True)
  return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
