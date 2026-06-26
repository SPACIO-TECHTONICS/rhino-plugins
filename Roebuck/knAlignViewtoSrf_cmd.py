"""Aligns the active viewport camera and construction plane (CPlane) to the normal of a selected surface face at the clicked location."""

import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knAlignViewtoSrf"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # get a surface face
    srf_info = rs.GetSurfaceObject("Select a surface to create CPlane and align view")
    if( srf_info != None ):
        srf_id = srf_info[0]
        pt = srf_info[3]
        
        # Get the U,V coordinates and exact plane at the clicked location
        uv = rs.SurfaceClosestPoint(srf_id, pt)
        if( uv != None ):
            plane = rs.SurfaceFrame(srf_id, uv)
            if( plane != None ):
                
                # Find an existing viewport that is NOT Top or Perspective
                views = rs.ViewNames()
                target_view = None
                for view in views:
                    if view.lower() not in ["top", "perspective"]:
                        target_view = view
                        break # Stop at the first valid alternative
                        
                if target_view != None:
                    # Make the chosen view active
                    rs.CurrentView(target_view)
                    
                    # Set the custom CPlane and align the camera to it
                    rs.ViewCPlane(target_view, plane)
                    rs.Command("-_Plan _Enter", False)
                else:
                    print "Could not find a suitable viewport. Please ensure Front, Right, or similar views are open."

    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

RunCommand(True)