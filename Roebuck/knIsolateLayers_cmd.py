# Isolate Layers
# ver 1.01
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.

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
