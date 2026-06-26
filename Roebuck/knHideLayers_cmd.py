# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan


import Rhino as r
import rhinoscriptsyntax as rs

__commandname__ = "knHideLayers"


def RunCommand(is_interactive):

    objs = rs.GetObjects("Select objects", preselect=True)

    if not objs:
        return r.Commands.Result.Failure
    rs.EnableRedraw(False)

    layers = [rs.ObjectLayer(obj) for obj in objs]

    for layer in layers:
        ObjstoHide = rs.ObjectsByLayer(layer, True)
        rs.HideObjects(ObjstoHide)

    rs.EnableRedraw(True)
    return r.Commands.Result.Success


if __name__ == "__main__":
    RunCommand(True)
