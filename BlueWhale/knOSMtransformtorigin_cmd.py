# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc

from assets import osm_logic
from assets import auth_helper
from assets.DrawRectangleDisplayNormal import DrawRectangleDisplayNormal

__commandname__ = "knOSMtransformtorigin"


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knOSMtransformtorigin"):
        return auth_helper.get_cancel_result()

    existing_matrix_str = rs.GetDocumentUserText("Transformation Matrix")
    existing_origin_str = rs.GetDocumentUserText("GeoLocated Origin")

    tol = sc.doc.ModelAbsoluteTolerance
    sc.doc.ModelAbsoluteTolerance = 0.01

    try:
        plane = DrawRectangleDisplayNormal()
        if not plane:
            print("Transformation canceled.")
            return Rhino.Commands.Result.Cancel

        objs = rs.AllObjects()
        if not objs:
            rs.MessageBox("No objects found in document to transform.")
            return Rhino.Commands.Result.Cancel

        new_matrix = rs.XformChangeBasis(rg.Plane.WorldXY, plane)

        combined_matrix = osm_logic.get_compound_matrix(existing_matrix_str, new_matrix)

        rs.TransformObjects(objs, new_matrix, False)

        rs.SetDocumentUserText("Transformation Matrix", str(combined_matrix))

        inverse_combined = rg.Transform.Empty
        success, inverse_combined = combined_matrix.TryGetInverse()
        if success:
            original_pt = rg.Point3d(0, 0, 0)
            original_pt.Transform(inverse_combined)

            new_lat = osm_logic.meters_to_lat(original_pt.Y)
            new_lon = osm_logic.meters_to_lon(original_pt.X)

            rs.SetDocumentUserText(
                "GeoLocated Origin", "{0}, {1}".format(new_lat, new_lon)
            )
            rs.SetDocumentUserText("Model Location", "Local")

            print(
                "Transformation compounded. New Geo-Origin: {0}, {1}".format(
                    new_lat, new_lon
                )
            )
        else:
            print("Warning: Could not calculate inverse matrix for geo-tracking.")

        return Rhino.Commands.Result.Success

    except Exception as e:
        import traceback

        print("Transformation Error: {0}".format(e))
        print(traceback.format_exc())
        return Rhino.Commands.Result.Failure
    finally:
        sc.doc.ModelAbsoluteTolerance = tol


if __name__ == "__main__":
    RunCommand(True)
