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

# WireframeDisplay
# ver 1.00
# 


import System.Guid, System.Drawing.Color
import Rhino.DocObjects as rd  # type: ignore
import Rhino as r  # type: ignore
import Rhino.Geometry  # type: ignore
import scriptcontext as sc  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knWireframeDisplay"


def RunCommand( is_interactive ):


guid = rs.GetObjects("Get Objects to display in wireframe")
    
    viewportId = sc.doc.Views.ActiveView.ActiveViewportID
    
    if (guid == None):
        print("The WireframeDisplay command was cancelled")
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
    
    if(x==True):
        print("The DisplayOverrides was removed")
    else:
        for obj in range(len(guid)):
            sc.doc.Objects.Select(guid[obj])
        
        rs.Command("_SetObjectDisplayMode _Wireframe")
        sc.doc.Objects.UnselectAll()
        sc.doc.Views.Redraw()

    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
