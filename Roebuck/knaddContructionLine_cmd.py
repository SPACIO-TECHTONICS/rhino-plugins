# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
import System.Drawing.Color

def RunCommand( is_interactive ):


    print("Executing " + __commandname__)

    point_a = rs.GetPoint("Pick First Point")
    if point_a:
        addConstructionLine(point_a)

def addConstructionLine(point_a):
    line_color_1 = System.Drawing.Color.FromArgb(200,200,200)
    line_color_2 = System.Drawing.Color.FromArgb(255,0,0)

    def GetPointDynamicDrawFunc( sender, args ):
        point_b = args.CurrentPoint
        point_C = Rhino.Geometry.Point3d((point_a.X + point_b.X)/2, (point_a.Y + point_b.Y)/2, (point_a.Z + point_b.Z)/2)
        vec = rs.VectorCreate(point_b, point_a)
        rs.VectorUnitize(vec)
        vec2 = rs.VectorScale(vec, 500)
        vec3 = rs.coerce3dpoint(rs.VectorAdd(point_b, vec2))
        rs.VectorReverse(vec2)
        vec4 = rs.coerce3dpoint(rs.VectorSubtract(point_b, vec2))
        
        args.Display.DrawLine(point_a, vec3, line_color_1, 1)
        args.Display.DrawLine(point_a, vec4, line_color_1, 1)
        args.Display.DrawPoint(point_a,Rhino.Display.PointStyle.ControlPoint,3,line_color_1)
        args.Display.DrawPoint(point_b,Rhino.Display.PointStyle.ControlPoint,3,line_color_2)

    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += GetPointDynamicDrawFunc
    gp.Get()
    if( gp.CommandResult() == Rhino.Commands.Result.Success ):
        pt = gp.Point()
        line = rs.AddLine(point_a, pt)
        c = rs.CurveMidPoint(line)
        scaled = rs.ScaleObject(line, c, [500, 500, 500])
        rs.ObjectColor(scaled, [199,199,199])


if( __name__ == "__main__" ):
    point_a = rs.GetPoint("Pick First Point")
    if point_a:
        addConstructionLine(point_a)

if __name__ == "__main__":
    RunCommand(True)
