import rhinoscriptsyntax as rs  # type: ignore
import Rhino.Geometry as rg  # type: ignore
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knAreainSF"

def RunCommand( is_interactive ):


print("Executing " + __commandname__)

    geos = rs.GetObjects("Select Geometries to measure area in SF", 
                         rs.filter.curve | rs.filter.surface | rs.filter.polysurface | rs.filter.mesh | rs.filter.extrusion,
                         preselect = True )
    if not geos: return

    # Calculate scale factor from doc units to Feet
    doc_unit_system = sc.doc.ModelUnitSystem
    scale = Rhino.RhinoMath.UnitScale(doc_unit_system, Rhino.UnitSystem.Feet)
    area_factor = scale * scale
    
    areatotal = 0.0
    validobjs = 0
    invalidobjs = 0
    
    for geo in geos:
        rhobj = rs.coercerhinoobject(geo, True, True)
        if rhobj:
            amp = rg.AreaMassProperties.Compute(rhobj.Geometry)
            if amp:
                areatotal += (amp.Area * area_factor)
                validobjs += 1
            else:
                if rs.IsCurve(geo) and rs.IsCurveClosed(geo):
                    areatotal += (rs.CurveArea(geo)[0] * area_factor)
                    validobjs += 1
                else:
                    invalidobjs += 1
        else:
            invalidobjs += 1
            
    print("Area in SF = {:,.2f} SF".format(areatotal))
    print("Invalid objects = {}".format(invalidobjs)) 
    print("Valid objects = {}".format(validobjs))
    
    rs.ClipboardText("{:.2f}".format(areatotal))
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
