# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino
import System.Drawing
import scriptcontext
import rhinoscriptsyntax as rs


class CustomConduit(Rhino.Display.DisplayConduit):
    def DrawForeground(self, e):
        color = System.Drawing.Color.Red
        bounds = e.Viewport.Bounds
        pt = Rhino.Geometry.Point2d(bounds.Right - 100, bounds.Bottom - 30)
        e.Display.Draw2dText("Hello", color, pt, False)

        col = System.Drawing.Color.Blue
        rectangle = System.Drawing.Rectangle(50, 100, 100, 100)
        e.Display.Draw2dRectangle(rectangle, color, 10, col)


def showafterscript():
    conduit = None
    if scriptcontext.sticky.has_key("myconduit"):
        conduit = scriptcontext.sticky["myconduit"]
    else:
        conduit = CustomConduit()
        scriptcontext.sticky["myconduit"] = conduit

    conduit.Enabled = not conduit.Enabled
    if conduit.Enabled:
        print("conduit enabled")
    else:
        print("conduit disabled")
    scriptcontext.doc.Views.Redraw()


def showinscript():
    conduit = CustomConduit()
    conduit.Enabled = True
    scriptcontext.doc.Views.Redraw()
    rs.GetString("Pausing for user input")
    conduit.Enabled = False
    scriptcontext.doc.Views.Redraw()


if __name__ == "__main__":
    showinscript()
