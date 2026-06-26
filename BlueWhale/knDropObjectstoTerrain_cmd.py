# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
from assets import auth_helper

__commandname__ = "knDropObjectstoTerrain"


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knDropObjectstoTerrain"):
        return auth_helper.get_cancel_result()

    objs = rs.GetObjects("Pick objects to drop", preselect=True)
    if not objs:
        return Rhino.Commands.Result.Cancel

    terrain = rs.GetObject(
        "Select terrain surface/mesh",
        filter=rs.filter.surface | rs.filter.polysurface | rs.filter.mesh,
    )
    if not terrain:
        return Rhino.Commands.Result.Cancel

    rs.EnableRedraw(False)
    try:
        for obj in objs:
            bbox = rs.BoundingBox(obj)
            if not bbox:
                continue

            bottom_center = (bbox[0] + bbox[2]) / 2.0

            pt_on_terrain = rs.ProjectPointToSurface(
                [bottom_center], terrain, [0, 0, -1]
            )
            if not pt_on_terrain:
                pt_on_terrain = rs.ProjectPointToSurface(
                    [bottom_center], terrain, [0, 0, 1]
                )

            if pt_on_terrain:
                translation = rs.VectorCreate(pt_on_terrain[0], bottom_center)
                rs.MoveObject(obj, translation)

        rs.EnableRedraw(True)
        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error dropping objects: {0}".format(e))
        return Rhino.Commands.Result.Failure


if __name__ == "__main__":
    RunCommand(True)
