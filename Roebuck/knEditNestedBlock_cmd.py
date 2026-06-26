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
