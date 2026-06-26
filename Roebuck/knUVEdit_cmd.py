from __future__ import print_function
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knUVEdit"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing", __commandname__)
    
    mesh_id = rs.GetObject("Select a mesh to edit its UVs", rs.filter.mesh)
    if not mesh_id: 
        return 1
        
    # Get existing UVs using native rhinoscriptsyntax
    uvs = rs.MeshTextureCoordinates(mesh_id)
    if not uvs:
        print("This mesh does not have existing texture coordinates.")
        return 1
        
    pt1 = rs.GetPoint("Click starting point for UV shift")
    if pt1 is None: 
        return 1
        
    pt2 = rs.GetPoint("Click target point", pt1)
    if pt2 is None: 
        return 1
        
    delta = pt2 - pt1
    uv_scale = 0.01 
    
    # Calculate the shift and format as a simple list of [u, v] lists
    new_uvs = []
    for uv in uvs:
        new_uvs.append([uv.X + (delta.X * uv_scale), uv.Y + (delta.Y * uv_scale)])
        
    # Apply the native Python list back to the mesh
    rs.MeshTextureCoordinates(mesh_id, new_uvs)
    print("UVs Shifted successfully.")
    
    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

if __name__ == "__main__":
    RunCommand(True)
