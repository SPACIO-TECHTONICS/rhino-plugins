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

"""Selects an annotation dot object and prints/returns its exact 3D coordinate point in the document."""

import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knGetDotPosition"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    #Select Annotation Dot
    obj=rs.GetObject("Select Annotation Dot",rs.filter.annotation)
    
    point = rs.coercerhinoobject(obj)
    
    print point.Geometry.Point
    
    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    #   0 == success
    #   1 == cancel
    # If this function does not return a value, success is assumed
    return 0

if __name__ == "__main__":
    RunCommand(True)
