# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

__commandname__ = "knEditDetailName"

def RunCommand( is_interactive ):


    pageview = sc.doc.Views.ActiveView
    
    if type(pageview) != Rhino.Display.RhinoPageView:
        rs.MessageBox("This tool only works in layout space.")
        return
    
    details = rs.GetObjects("Select detail(s) to name",32768, preselect=True)
    for detail in details:
        rs.SelectObject(detail)
        name = rs.StringBox("Enter the name of the selected detail")
        rs.ObjectName(detail,name)
        rs.UnselectAllObjects()
    return

if __name__ == "__main__":
    RunCommand(True)
