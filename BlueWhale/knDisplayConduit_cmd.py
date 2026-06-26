"""Provides a dynamic, real-time screen-space overlay of object areas. Displays individual object area labels directly on the viewport, along with a running total area readout in the top-left corner."""

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore
import System.Drawing.Color as Color  # type: ignore
from assets import auth_helper

__commandname__ = "knDisplayConduit"

class DynamicAreaConduit(Rhino.Display.DisplayConduit):
    def __init__(self, object_ids):
        self.object_ids = object_ids

    def DrawForeground(self, e):
        total_area = 0.0
        e.Display.Draw2dText("AREA AUDIT ACTIVE", Color.Black, Rhino.Geometry.Point2d(20, 20), False, 24)
        e.Display.Draw2dText("Run command again to clear graphics.", Color.DarkGray, Rhino.Geometry.Point2d(20, 85), False, 14)

        for obj_id in self.object_ids:
            rh_obj = sc.doc.Objects.FindId(obj_id)
            if not rh_obj or rh_obj.IsDeleted:
                continue
                
            geom = rh_obj.Geometry
            area = 0.0
            
            if isinstance(geom, Rhino.Geometry.Curve) and geom.IsClosed:
                amp = Rhino.Geometry.AreaMassProperties.Compute(geom)
                if amp: area = amp.Area
            elif isinstance(geom, (Rhino.Geometry.Brep, Rhino.Geometry.Surface, Rhino.Geometry.Extrusion)):
                amp = Rhino.Geometry.AreaMassProperties.Compute(geom)
                if amp: area = amp.Area
                
            if area > 0:
                total_area += area
                bbox = geom.GetBoundingBox(True)
                if bbox.IsValid:
                    center = bbox.Center
                    e.Display.DrawDot(center, "{0:.1f} sf".format(area), Color.DarkOrange, Color.White)

        e.Display.Draw2dText("Total Area: {0:.2f} sf".format(total_area), Color.Blue, Rhino.Geometry.Point2d(20, 55), False, 18)

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knDisplayConduit"):
        return auth_helper.get_cancel_result()

    conduit_key = "kn_DynamicAreaConduit_Active"
    
    if sc.sticky.has_key(conduit_key):
        conduit = sc.sticky[conduit_key]
        conduit.Enabled = False
        del sc.sticky[conduit_key]
        sc.doc.Views.Redraw()
        print("Display conduit disabled.")
        return Rhino.Commands.Result.Success
        
    object_ids = rs.GetObjects("Select closed curves or surfaces to audit area dynamically", rs.filter.curve | rs.filter.surface | rs.filter.polysurface, preselect=True)
    
    if not object_ids:
        return Rhino.Commands.Result.Cancel
        
    conduit = DynamicAreaConduit(object_ids)
    conduit.Enabled = True
    sc.sticky[conduit_key] = conduit
    sc.doc.Views.Redraw()
    
    print("Dynamic display conduit enabled. Try scaling or moving the objects.")
    return Rhino.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
