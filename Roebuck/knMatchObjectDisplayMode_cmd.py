import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino.Display as rd  # type: ignore
import Rhino as r  # type: ignore

__commandname__ = "knMatchObjectDisplayMode"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


objIDs=rs.GetObjects("Get Objects whose display modes to change",8+16+32,preselect=True)
    if not objIDs: return
    
    all_dmodes = rd.DisplayModeDescription.GetDisplayModes()
    if not all_dmodes:
        print("Failed to get display mode data!") ; return
    
    #check display modes for validity and create 2 parallel lists modes/names
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
    
    print (valid_dmodes)
    
    
    
    sourceID = rs.GetObject("Get Source Object",8+16+32,preselect=True)
    if not sourceID: return
    
    vID = sc.doc.Views.ActiveView.ActiveViewportID
    
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
    
    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
