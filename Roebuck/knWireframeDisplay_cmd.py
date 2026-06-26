# WireframeDisplay
# ver 1.00
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.


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
