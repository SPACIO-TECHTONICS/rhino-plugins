# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan


import rhinoscriptsyntax as rs
import Rhino as r

__commandname__ = "knIsolateLayers"


def RunCommand(is_interactive):

    objs = rs.GetObjects("Select the objects", preselect=True)
    rs.UnselectAllObjects()
    if not objs:
        return r.Commands.Result.Failure
    rs.EnableRedraw(False)

    layers = [rs.ObjectLayer(obj) for obj in objs]
    for layer in layers:
        ObjstoShow = rs.ObjectsByLayer(layer, True)
        rs.SelectObjects(ObjstoShow)

    invobjs = rs.InvertSelectedObjects()

    rs.HideObjects(invobjs)
    rs.EnableRedraw(True)
    return r.Commands.Result.Success


if __name__ == "__main__":
    RunCommand(True)
