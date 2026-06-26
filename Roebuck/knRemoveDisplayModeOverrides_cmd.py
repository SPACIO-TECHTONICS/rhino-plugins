import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino.DocObjects as rd  # type: ignore
import Rhino as r  # type: ignore

__commandname__ = "knRemoveDisplayModeOverrides"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
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
