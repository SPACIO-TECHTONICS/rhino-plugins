# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

__commandname__ = "knEditNestedBlock" 

def RunCommand( is_interactive ):


    print("Executing " + __commandname__)
    
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt("Select a block (Ctrl+Shift+Click for nested blocks)")
    go.GeometryFilter = Rhino.DocObjects.ObjectType.InstanceReference
    go.SubObjectSelect = True
    go.Get()
    
    if go.CommandResult() != Rhino.Commands.Result.Success:
        return 1
        
    objref = go.Object(0)
    geom = objref.Geometry()
    
    if isinstance(geom, Rhino.Geometry.InstanceReferenceGeometry):
        idef_id = geom.ParentIdefId
        idef = sc.doc.InstanceDefinitions.FindId(idef_id)
        
        if idef:
            block_name = idef.Name
            print("Editing block: " + block_name)
            rs.Command("-_BlockEdit " + chr(34) + block_name + chr(34))
            return 0
    else:
        print("Selection was not a valid block instance.")
        return 1

    return 0

if __name__ == "__main__":
    RunCommand(True)
