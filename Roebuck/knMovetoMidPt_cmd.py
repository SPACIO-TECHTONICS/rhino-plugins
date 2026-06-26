# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Moves selected objects from a base point to the exact midpoint between two clicked target points or to a point along a curve."""

import rhinoscriptsyntax as rs

__commandname__ = "knMovetoMidPt"


def RunCommand(is_interactive):

    objIds = rs.GetObjects("Select objects to move", preselect=True)
    if not objIds:
        return 1

    base_pt = rs.GetPoint("Select base point (point to move from)")
    if not base_pt:
        return 1

    pt1 = rs.GetPoint("Select first target point (or press Enter to select a curve)")

    if pt1:
        pt2 = rs.GetPoint("Select second target point", base_point=pt1)
        if not pt2:
            return 1
        mid_pt = (pt1 + pt2) / 2.0
    else:
        target = rs.GetObject(
            "Select target line or curve for midpoint alignment",
            rs.filter.curve | rs.filter.edgeobject,
        )
        if not target:
            return 1

        curve = rs.coercecurve(target)
        if not curve:
            print("Invalid target: not a curve or edge.")
            return 1
        mid_pt = curve.PointAtNormalizedParameter(0.5)

    translation = mid_pt - base_pt
    rs.MoveObjects(objIds, translation)

    print("Moved {} objects to midpoint.".format(len(objIds)))

    return 0


if __name__ == "__main__":
    RunCommand(True)
