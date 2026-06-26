# Delete Layers
# ver 1.00
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.


import System.Guid, System.Drawing.Color
import Rhino.DocObjects as rd  # type: ignore
import Rhino as r  # type: ignore
import scriptcontext as sc  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knDeleteLayers"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


layerlist = []
    for layer in sc.doc.ActiveDoc.Layers:
        #print(layer)
        layerlist.Add(layer.Name)
    
    layerlist = list(filter(None,layerlist))
    
    str = rs.GetString("Type the layer to delete")
    
    if(str == None):
        return r.Commands.Result.Failure
    
    indices = [i for i, s in enumerate(layerlist) if str in s]
    
    if(len(indices) == 0):
        print("No such layer found in document")
        return r.Commands.Result.Failure

    #print(layerlist)
    
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
