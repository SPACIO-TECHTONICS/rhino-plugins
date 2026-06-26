# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan


import Rhino as r
import scriptcontext as sc
import rhinoscriptsyntax as rs



__commandname__ = "knImportWorksessionFiles"

def RunCommand( is_interactive ):


items = ("Select", "No", "Yes")
    results = rs.GetBoolean("Save as different file?", items, (True) )
    
    if(results[0] == True):
        rs.Command("SaveAs")
        
    ws = sc.doc.Worksession
    if not ws: 
        return r.Commands.Result.Failure
    
    paths = ws.ModelPaths
    if not paths:
        return r.Commands.Result.Failure
    
    filepath = rs.DocumentPath()
    filename = rs.DocumentName()
    
    file = filepath+filename
    
    if(file==paths[0]):
        print("There is no active worksession file")
        return r.Commands.Result.Failure
    else:
        for path in paths:
            rs.Command("_-Import " + path + " _Enter")

    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
