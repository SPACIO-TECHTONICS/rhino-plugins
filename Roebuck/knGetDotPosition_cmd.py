# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Selects an annotation dot object and prints/returns its exact 3D coordinate point in the document."""

import rhinoscriptsyntax as rs

__commandname__ = "knGetDotPosition"

def RunCommand( is_interactive ):


    print("Executing " + __commandname__)
    
    obj=rs.GetObject("Select Annotation Dot",rs.filter.annotation)
    
    point = rs.coercerhinoobject(obj)
    
    print point.Geometry.Point
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
