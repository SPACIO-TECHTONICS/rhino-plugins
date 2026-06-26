# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc
from assets import osm_utilities
from assets import ui_osm3d
from assets import auth_helper

__commandname__ = "knRoadfromCrv"


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knRoadfromCrv"):
        return auth_helper.get_cancel_result()

    values = ui_osm3d.show_eto_form_with_titles(
        "Road Creation Toolbox", "Width of Road", "Radius of Rotation"
    )
    if not values:
        return Rhino.Commands.Result.Cancel

    offset = values.get("Width of Road", 5.0)
    radius = values.get("Radius of Rotation", 10.0)

    crv_ids = rs.GetObjects("Select Curves", rs.filter.curve)
    if not crv_ids:
        return Rhino.Commands.Result.Cancel

    rs.EnableRedraw(False)
    final_crv_ids = []

    try:
        for crv_id in crv_ids:
            crv_geom = rs.coercecurve(crv_id)
            if not crv_geom:
                continue

            filleted = rg.Curve.CreateFilletCornersCurve(
                crv_geom,
                radius,
                sc.doc.ModelAbsoluteTolerance,
                sc.doc.ModelAngleToleranceDegrees,
            )
            if not filleted:
                filleted = crv_geom

            temp_crv_id = sc.doc.Objects.AddCurve(filleted)

            start_pt = rs.CurveStartPoint(temp_crv_id)
            test_pt = rg.Point3d(start_pt.X + offset, start_pt.Y, start_pt.Z)

            crv1_id = rs.OffsetCurve(temp_crv_id, test_pt, offset)
            crv2_id = rs.OffsetCurve(temp_crv_id, test_pt, -offset)

            if crv1_id and crv2_id:
                pt1 = rs.CurveStartPoint(crv1_id)
                pt2 = rs.CurveStartPoint(crv2_id)
                pt3 = rs.CurveEndPoint(crv1_id)
                pt4 = rs.CurveEndPoint(crv2_id)

                l1 = rs.AddLine(pt1, pt2)
                l2 = rs.AddLine(pt3, pt4)

                joined = rs.JoinCurves([crv1_id, crv2_id, l1, l2], True)
                for j_id in joined:
                    if rs.IsCurveClosed(j_id):
                        final_crv_ids.append(j_id)
                    else:
                        rs.DeleteObject(j_id)

            rs.DeleteObject(temp_crv_id)

        if not final_crv_ids:
            rs.EnableRedraw(True)
            return Rhino.Commands.Result.Failure

        unioned_ids = rs.CurveBooleanUnion(final_crv_ids)
        if unioned_ids:
            osm_utilities.CreatePlanarSrfsfromCurves(unioned_ids)
            rs.DeleteObjects(unioned_ids)

        rs.DeleteObjects(final_crv_ids)
        rs.EnableRedraw(True)
        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error creating roads: {0}".format(e))
        return Rhino.Commands.Result.Failure


if __name__ == "__main__":
    RunCommand(True)
