# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import Rhino
import rhinoscriptsyntax as rs

def RunCommand(is_interactive):


    views = Rhino.RhinoDoc.ActiveDoc.Views.GetPageViews()

    print(views)

    for view in views:
        view.SetPageAsActive()

if __name__ == "__main__":
    RunCommand(True)
