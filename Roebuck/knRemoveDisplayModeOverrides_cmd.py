# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino.DocObjects as rd
import Rhino as r

__commandname__ = "knRemoveDisplayModeOverrides"

def RunCommand( is_interactive ):


guid = rs.GetObjects("Set Objects to remove overrides")
    
    viewportId = sc.doc.Views.ActiveView.ActiveViewportID
    
    if (guid == None):
        print("The command was cancelled")
        return r.Commands.Result.Failure
    
    
    objref = []
    x = False
    for obj in range(len(guid)):
        object = rd.ObjRef(guid[obj])
        attr = object.Object().Attributes
        if attr.HasDisplayModeOverride(viewportId):
            attr.RemoveDisplayModeOverride(viewportId)
            sc.doc.Objects.ModifyAttributes(object, attr, False)
            x=True
        objref.Add(object)
    
    sc.doc.Views.Redraw()
    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
