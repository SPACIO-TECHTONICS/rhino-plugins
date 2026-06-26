import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knChangeBlockName"

def RunCommand( is_interactive ):


# Get current block name
    block_names = rs.BlockNames()
    if not block_names:
        print("No blocks found in document.")
        return 1
        
    old_name = rs.ListBox(block_names, "Select block to rename", "Rename Block")
    if not old_name:
        return 1
        
    new_name = rs.StringBox("Enter new name for block '{}'".format(old_name), old_name, "Rename Block")
    if not new_name or new_name == old_name:
        return 1
        
    if rs.IsBlock(new_name):
        print("A block with name '{}' already exists.".format(new_name))
        return 1
        
    # Use rs.RenameBlock if available, otherwise we'd need to modify definition
    # Note: rhinoscriptsyntax doesn't have RenameBlock directly in all versions, 
    # but we can use rs.Command as a fallback or RhinoCommon.
    
    import Rhino
    import scriptcontext as sc
    
    idef = sc.doc.InstanceDefinitions.Find(old_name)
    if idef:
        sc.doc.InstanceDefinitions.Modify(idef.Index, new_name, idef.Description, True)
        print("Renamed block '{}' to '{}'".format(old_name, new_name))
        return 0
    
    return 1

if __name__ == "__main__":
    RunCommand(True)
