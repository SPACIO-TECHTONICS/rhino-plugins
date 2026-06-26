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
import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore

__commandname__ = "knEditDetailName"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


pageview = sc.doc.Views.ActiveView
    
    if type(pageview) != Rhino.Display.RhinoPageView:
        rs.MessageBox("This tool only works in layout space.")
        #print "This tool only works in layout space."
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
