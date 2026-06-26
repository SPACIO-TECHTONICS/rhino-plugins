import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knEditNestedBlock" 

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    # Use RhinoCommon GetObject to allow sub-object selection of nested blocks
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt("Select a block (Ctrl+Shift+Click for nested blocks)")
    go.GeometryFilter = Rhino.DocObjects.ObjectType.InstanceReference
    go.SubObjectSelect = True
    go.Get()
    
    if go.CommandResult() != Rhino.Commands.Result.Success:
        return 1 # Cancel
        
    objref = go.Object(0)
    geom = objref.Geometry()
    
    # Check if the selected geometry is a block instance
    if isinstance(geom, Rhino.Geometry.InstanceReferenceGeometry):
        idef_id = geom.ParentIdefId
        idef = sc.doc.InstanceDefinitions.FindId(idef_id)
        
        if idef:
            block_name = idef.Name
            print("Editing block: " + block_name)
            # Run the native block edit command with the specific definition name
            rs.Command("-_BlockEdit " + chr(34) + block_name + chr(34))
            return 0 # Success
    else:
        print("Selection was not a valid block instance.")
        return 1

    return 0

if __name__ == "__main__":
    RunCommand(True)
