# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan


import Rhino
import System


def DrawRectangleDisplayNormal():

    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("First point")
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return
    point_a = gp.Point()

    gp.SetCommandPrompt("Second point")
    gp.SetBasePoint(point_a, True)
    gp.DrawLineFromPoint(point_a, True)
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return
    point_b = gp.Point()

    def RectangleFrom3Points(a, b, c):

        plane = Rhino.Geometry.Plane(a, b, c)
        if not plane.IsValid:
            return

        width = a.DistanceTo(b)
        line = Rhino.Geometry.Line(a, b)
        height = line.DistanceTo(c, False)

        rect = Rhino.Geometry.Rectangle3d(plane, width, height)
        if rect:
            return rect

    def OnDynamicDraw(self, e):

        color = System.Drawing.Color.Red

        rect = RectangleFrom3Points(point_a, point_b, e.CurrentPoint)
        if not rect:
            return

        e.Display.DrawPolyline(rect.ToPolyline(), color, 2)
        e.Display.DrawDirectionArrow(rect.Center, rect.Plane.Normal, color)

    gp.SetCommandPrompt("Third point")
    gp.EnableDrawLineFromPoint(False)
    gp.DynamicDraw += OnDynamicDraw
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return
    point_c = gp.Point()

    rect = RectangleFrom3Points(point_a, point_b, point_c)

    if rect:
        return rect.Plane
    else:
        return

    gp.Dispose()


DrawRectangleDisplayNormal()
