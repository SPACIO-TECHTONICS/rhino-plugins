import rhinoscriptsyntax as rs

__commandname__ = "knCircleOnSrf"

# RunCommand is called when the user enters the command name in Rhino.
# The command name is defined by the filename minus "_cmd.py"
def RunCommand( is_interactive ):
    print "Running", __commandname__
    
    # Select the target surface
    srf_id = rs.GetSurfaceObject("Select surface for circle placement", preselect=True)
    if not srf_id:
        return 1 # cancel
        
    surface = srf_id[0]
    
    # Get the center point on the surface
    point = rs.GetPointOnSurface(surface, "Pick circle center point on surface")
    if point is None:
        return 1 # cancel
        
    # Get the radius for the circle (fixed keyword argument here)
    radius = rs.GetReal("Circle radius", 1.0, minimum=0.0)
    if radius is None:
        return 1 # cancel
        
    # Find the UV parameter of the picked point on the surface
    uv = rs.SurfaceClosestPoint(surface, point)
    
    # Evaluate the surface normal vector at that UV parameter
    normal = rs.SurfaceNormal(surface, uv)
    
    if normal:
        # Create a plane centered at the point with the normal as the Z-axis
        plane = rs.PlaneFromNormal(point, normal)
        # Add the circle to the document using the plane and radius
        rs.AddCircle(plane, radius)
        return 0 # success
        
    return 1 # cancel

RunCommand(True)