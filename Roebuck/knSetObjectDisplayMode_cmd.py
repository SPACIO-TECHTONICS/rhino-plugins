# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import rhinoscriptsyntax as rs
import Rhino as r
import scriptcontext as sc

__commandname__ = "knSetObjectDisplayMode"

def RunCommand( is_interactive ):


    objIDs=rs.GetObjects("Get Objects whose display modes to change",8+16+32,preselect=True)
    if not objIDs: return
    
    
    all_dmodes = r.Display.DisplayModeDescription.GetDisplayModes()
    if not all_dmodes:
        print("Failed to get display mode data!") ; return
    valid_dmodes=[]
    valid_modenames=[]
    for dmode in all_dmodes:
        if dmode is not None and not dmode.PipelineLocked:
            local_name=dmode.LocalName
            if local_name:
                valid_dmodes.append(dmode)
                valid_modenames.append(local_name)
    if not valid_dmodes:
        print("No valid display modes found!") ; return
    
    mode_name=rs.ListBox(valid_modenames,"Choose a display mode for objects","Display Mode List")
    if not mode_name: return
    
    vID = sc.doc.Views.ActiveView.ActiveViewportID
    
    for dmode in valid_dmodes:
        if dmode.LocalName == mode_name:
            for obj in objIDs:
                object = r.DocObjects.ObjRef(obj)
                attr = object.Object().Attributes
                attr.SetDisplayModeOverride(dmode, vID)
                sc.doc.Objects.ModifyAttributes(obj, attr, False)
    
    sc.doc.Views.Redraw()
    
    """
    sourceRef = sc.doc.Objects.Find(sourceID)
    sourceAttr = sourceRef.Attributes
    sourceDModeID = sourceAttr.GetDisplayModeOverride(vID)
    print sourceDModeID
    
    for dmode in valid_dmodes:
        if sourceDModeID == dmode.Id:
            print("found")
            for objID in objIDs:
                objRef=sc.doc.Objects.Find(objID)
                attr = objRef.Attributes
                attr.SetDisplayModeOverride(dmode, vID)
                sc.doc.Objects.ModifyAttributes(objID, attr, False)
    
    sc.doc.Views.Redraw()
    """
    
    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
