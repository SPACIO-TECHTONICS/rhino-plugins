"""Orients a selected block instance onto a planar surface, with options to align using the block's native reference plane or a flat World Z-normal plane."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore

__commandname__ = "knOrientonSrf" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):


print("Executing"), __commandname__
    
    # Select the block instance
    block_id = rs.GetObject("Select a block instance to orient", rs.filter.instance)
    if block_id is None: 
        return 1
        
    # Ask the user if they want to use the block's own reference plane
    use_ref = rs.GetString("Use the block's reference plane as the source plane?", "Yes", ["Yes", "No"])
    if use_ref is None:
        return 1
        
    # Select the planar surface
    srf_id = rs.GetObject("Select a planar surface", rs.filter.surface)
    if srf_id is None: 
        return 1
        
    # Verify the surface is planar
    if not rs.IsSurfacePlanar(srf_id):
        print("The selected surface is not planar.")
        return 1
        
    # Get the parameter at the center of the surface domain
    u_domain = rs.SurfaceDomain(srf_id, 0)
    v_domain = rs.SurfaceDomain(srf_id, 1)
    u_mid = u_domain[0] + (u_domain[1] - u_domain[0]) / 2.0
    v_mid = v_domain[0] + (v_domain[1] - v_domain[0]) / 2.0
    
    # Extract the target plane from the surface frame
    target_plane = rs.SurfaceFrame(srf_id, [u_mid, v_mid])
    
    # Determine the source plane based on user preference
    insert_pt = rs.BlockInstanceInsertPoint(block_id)
    
    if use_ref.lower() == "yes":
        # Extract the block's local reference plane using its transform matrix
        xform_block = rs.BlockInstanceXform(block_id)
        
        # Transform the base origin and axes to find the block's current local plane
        pt_origin = rs.PointTransform([0,0,0], xform_block)
        pt_x = rs.PointTransform([1,0,0], xform_block)
        pt_y = rs.PointTransform([0,1,0], xform_block)
        
        vec_x = rs.VectorCreate(pt_x, pt_origin)
        vec_y = rs.VectorCreate(pt_y, pt_origin)
        
        source_plane = rs.PlaneFromFrame(pt_origin, vec_x, vec_y)
    else:
        # Default to a flat World Z-normal plane at the insertion point
        source_plane = rs.PlaneFromNormal(insert_pt, [0, 0, 1])
    
    # Create a Plane-to-Plane transformation matrix
    xform_orient = Rhino.Geometry.Transform.PlaneToPlane(source_plane, target_plane)
    
    # Apply the transformation to the block
    rs.TransformObject(block_id, xform_orient, copy=True)
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
