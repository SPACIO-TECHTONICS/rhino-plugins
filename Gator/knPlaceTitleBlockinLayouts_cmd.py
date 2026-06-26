# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

def RunCommand(is_interactive):


views = Rhino.RhinoDoc.ActiveDoc.Views.GetPageViews()

    print(views)

    for view in views:
        view.SetPageAsActive()
        # Rhino.RhinoDoc.InstanceDefinitions.Find()
        # rs.InsertBlock("STT-A2TitleBlock_PanellingStructure",(0,0,0),(1,1,1))

if __name__ == "__main__":
    RunCommand(True)
