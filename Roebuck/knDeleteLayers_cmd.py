# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan



import System.Guid, System.Drawing.Color
import Rhino.DocObjects as rd
import Rhino as r
import scriptcontext as sc
import rhinoscriptsyntax as rs

__commandname__ = "knDeleteLayers"

def RunCommand( is_interactive ):


layerlist = []
    for layer in sc.doc.ActiveDoc.Layers:
        layerlist.Add(layer.Name)
    
    layerlist = list(filter(None,layerlist))
    
    str = rs.GetString("Type the layer to delete")
    
    if(str == None):
        return r.Commands.Result.Failure
    
    indices = [i for i, s in enumerate(layerlist) if str in s]
    
    if(len(indices) == 0):
        print("No such layer found in document")
        return r.Commands.Result.Failure

    
    matchingLayers = [layer for layer in sc.doc.Layers if layer.Name == str]
    
    if(len(matchingLayers) == 0):
        print("No such layer found in document")
        return r.Commands.Result.Failure
    else:
        layerToUnlock = matchingLayers[0]
        if layerToUnlock.IsLocked:
            layerToUnlock.IsLocked = False
            layerToUnlock.CommitChanges()
        
        for layer in range(len(indices)):
            objs = sc.doc.Objects.FindByLayer(layerlist[indices[layer]])
            for obj in range(len(objs)): 
                sc.doc.Objects.Delete(objs[obj])
            rs.Command("Purge Enter")
        
    sc.doc.Views.Redraw()
    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
