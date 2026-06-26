# Hide Layers
# ver 1.00
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.

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
