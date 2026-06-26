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
import Rhino.Geometry as rg  # type: ignore
import Rhino.Commands  # type: ignore
import scriptcontext as sc  # type: ignore
from assets import osm_utilities
from assets import ui_osm3d
from assets import auth_helper

__commandname__ = "knDrawRoad"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knDrawRoad"):
        return auth_helper.get_cancel_result()

    values = ui_osm3d.show_eto_form_with_titles("Draw Road Toolbox", "Width of Road", "Radius")
    if not values:
        return Rhino.Commands.Result.Cancel
    
    # Eto forms often return dictionaries with titles as keys
    offset = values.get("Width of Road", 10.0)
    radius = values.get("Radius", 10.0)
    
    pts = rs.GetPoints(True, message1="Pick first point", message2="Pick next point or press Enter to end", max_points=99)
    if not pts or len(pts) < 2:
        return Rhino.Commands.Result.Cancel

    try:
        crv_id = rs.AddPolyline(pts)
        crv_obj = rs.coercecurve(crv_id)
        
        # Self-intersection check
        intersection_events = rg.Intersect.Intersection.CurveSelf(crv_obj, sc.doc.ModelAbsoluteTolerance)
        if intersection_events.Count > 0:
            rs.MessageBox("The command only works with non-self intersecting curves.")
            rs.DeleteObject(crv_id)
            return Rhino.Commands.Result.Failure

        # Fillet corners
        if len(pts) > 2:
            filleted_crv = rg.Curve.CreateFilletCornersCurve(crv_obj, radius, sc.doc.ModelAbsoluteTolerance, sc.doc.ModelAngleToleranceDegrees)
            crv0_id = sc.doc.Objects.AddCurve(filleted_crv)
        else:
            crv0_id = sc.doc.Objects.AddCurve(crv_obj)
            
        # Offsets
        start_pt = rs.CurveStartPoint(crv0_id)
        test_pt = rg.Point3d(start_pt.X + offset, start_pt.Y, start_pt.Z)
        
        crv1_id = rs.OffsetCurve(crv0_id, test_pt, offset)
        crv2_id = rs.OffsetCurve(crv0_id, test_pt, -offset)
        
        if not crv1_id or not crv2_id:
            print("Failed to offset curves.")
            return Rhino.Commands.Result.Failure

        # Join to create closed boundary
        pt1 = rs.CurveStartPoint(crv1_id)
        pt2 = rs.CurveStartPoint(crv2_id)
        pt3 = rs.CurveEndPoint(crv1_id)
        pt4 = rs.CurveEndPoint(crv2_id)
        
        l1 = rs.AddLine(pt1, pt2)
        l2 = rs.AddLine(pt3, pt4)
        
        joined_ids = rs.JoinCurves([crv1_id, crv2_id, l1, l2], True)
        final_boundary_ids = []
        for j_id in joined_ids:
            if rs.IsCurveClosed(j_id):
                final_boundary_ids.append(j_id)
            else:
                rs.DeleteObject(j_id)
        
        if final_boundary_ids:
            osm_utilities.CreatePlanarSrfsfromCurves(final_boundary_ids)
            rs.DeleteObjects(final_boundary_ids)
            
        # Cleanup
        rs.DeleteObjects([crv_id, crv0_id])
        return Rhino.Commands.Result.Success

    except Exception as e:
        import traceback
        print("Error in DrawRoad: {0}".format(e))
        print(traceback.format_exc())
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
