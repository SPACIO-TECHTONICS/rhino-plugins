# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
import re
from assets import auth_helper

__commandname__ = "knCrossCheckAreas"


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knCrossCheckAreas"):
        return auth_helper.get_cancel_result()

    mode = rs.GetString("Choose selection mode", "Select", ["EntireDocument", "Select"])
    if mode == "EntireDocument":
        objects = rs.ObjectsByType(8 | 16)
        if not objects:
            print("No breps found in the document.")
            return Rhino.Commands.Result.Failure
    elif mode == "Select":
        objects = rs.GetObjects(
            "Select breps to check projected areas", filter=8 | 16, preselect=True
        )
        if not objects:
            return Rhino.Commands.Result.Cancel
    else:
        return Rhino.Commands.Result.Cancel

    tolerance = rs.UnitAbsoluteTolerance()

    temp_layer = "Temp_Mismatch_Dots"
    if not rs.IsLayer(temp_layer):
        rs.AddLayer(temp_layer, color=rs.CreateColor(255, 0, 0))

    created_dots = []

    for obj in objects:
        name = rs.ObjectName(obj)
        if not name:
            continue

        match = re.search(r"([-+]?\d*\.\d+|\d+)\s*(sf|sq\.m)", name, re.IGNORECASE)
        if not match:
            continue

        expected_area = float(match.group(1))
        brep = rs.coercebrep(obj)
        if not brep:
            continue

        meshes = Rhino.Geometry.Mesh.CreateFromBrep(
            brep, Rhino.Geometry.MeshingParameters.FastRenderMesh
        )
        if not meshes:
            continue

        combined_mesh = Rhino.Geometry.Mesh()
        for m in meshes:
            combined_mesh.Append(m)

        outlines = combined_mesh.GetOutlines(Rhino.Geometry.Plane.WorldXY)
        if not outlines:
            continue

        curves = [Rhino.Geometry.PolylineCurve(poly) for poly in outlines]
        area = None
        planar_breps = Rhino.Geometry.Brep.CreatePlanarBreps(curves, tolerance)

        if planar_breps:
            area = sum([pb.GetArea() for pb in planar_breps])
        else:
            union_curves = Rhino.Geometry.Curve.CreateBooleanUnion(curves, tolerance)
            if union_curves:
                planar_breps_union = Rhino.Geometry.Brep.CreatePlanarBreps(
                    union_curves, tolerance
                )
                if planar_breps_union:
                    area = sum([pb.GetArea() for pb in planar_breps_union])

        if area is not None:
            diff = abs(expected_area - area)
            if diff <= tolerance:
                print(
                    "MATCH: {0} (Expected: {1}, Calculated XY: {2:.4f})".format(
                        name, expected_area, area
                    )
                )
            else:
                print(
                    "MISMATCH: {0} (Expected: {1}, Calculated XY: {2:.4f})".format(
                        name, expected_area, area
                    )
                )

                bbox = rs.BoundingBox(obj)
                if bbox:
                    center_pt = (bbox[0] + bbox[6]) / 2
                    dot_text = "Exp: {0} | Calc: {1:.1f}".format(expected_area, area)
                    dot_id = rs.AddTextDot(dot_text, center_pt)
                    rs.ObjectLayer(dot_id, temp_layer)
                    created_dots.append(dot_id)
        else:
            print("Could not calculate projected area for object: {0}".format(name))

    if created_dots:
        rs.Redraw()
        rs.GetString(
            "{0} mismatches found! Press Enter/Space to clear text dots...".format(
                len(created_dots)
            )
        )
        rs.DeleteObjects(created_dots)
        if rs.IsLayerEmpty(temp_layer):
            rs.DeleteLayer(temp_layer)
    else:
        print("All checked objects match their expected areas!")
        if rs.IsLayerEmpty(temp_layer):
            rs.DeleteLayer(temp_layer)

    return Rhino.Commands.Result.Success


if __name__ == "__main__":
    RunCommand(True)
