# Import Worksession Files
# ver 1.00
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.

import Rhino as r  # type: ignore
import scriptcontext as sc  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore



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
