# Planarize Surface
# ver 1.00
# By Keshava Narayan
# keshavanarayan82@gmail.com
# 
# This command is licensed under a Creative Commons 
# Attribution-NonCommercial-ShareAlike 4.0 International License.


import System.Guid, System.Drawing.Color
import Rhino.DocObjects as rd  # type: ignore
import Rhino as r  # type: ignore
import scriptcontext as sc  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knPlanarizeSurface"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing"), __commandname__
    
    
    guid = rs.GetSurfaceObject("Select surface to planarize",True, True)
    
    
    if (guid == None):
        print("The PlanarizeSurface command was cancelled")
        return r.Commands.Result.Failure
        
    surface_obj = rs.coercesurface(guid[0])
    
    if (surface_obj.IsPlanar() == True):
        print("The surface is planar")
        #rs.AddTextDot("The surface is planar",surface_obj.PointAt(0.5, 0.5))
        sc.doc.Objects.UnselectAll()
        sc.doc.Views.Redraw()
        return r.Commands.Result.Success
    
    else:
        
        curve = rs.DuplicateSurfaceBorder(guid[0])
        curve_obj = rs.coercecurve(curve[0])
        rs.DeleteObject(curve[0])
        
        domain0 = r.Geometry.Interval(0,1)
        domain1 = r.Geometry.Interval(0,1)
        
        surface_obj.SetDomain(0, domain0)
        surface_obj.SetDomain(1, domain1)
        vec = surface_obj.NormalAt(0.5,0.5)
        vec.Reverse()
        plane = r.Geometry.Plane(surface_obj.PointAt(0.5, 0.5),vec)
        
        
        cobj = r.Geometry.Curve.DuplicateCurve(curve_obj)
        planarcurve = r.Geometry.Curve.ProjectToPlane(cobj,plane)
        surface = r.Geometry.Brep.CreatePlanarBreps(planarcurve)
        
        sc.doc.ActiveDoc.Objects.AddBrep(surface[0])
        
    sc.doc.Objects.UnselectAll()
    sc.doc.Views.Redraw()


    return r.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
