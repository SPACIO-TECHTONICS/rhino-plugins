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

import rhinoscriptsyntax as rs  # type: ignore
import Rhino as r  # type: ignore



__commandname__ = "knIsolateGroups"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


gnames = rs.GroupNames()
    
    for name in gnames:
        rs.Command("-SelGroup " + name)
    
    rs.Command("Isolate")

if __name__ == "__main__":
    RunCommand(True)
