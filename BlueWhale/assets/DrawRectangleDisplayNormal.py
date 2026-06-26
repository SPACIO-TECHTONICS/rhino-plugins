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

# draw rectangle and displays its normal (c) 2019, Clement Greiner, CG3D

import Rhino  # type: ignore
import scriptcontext  # type: ignore
import System  # type: ignore

def DrawRectangleDisplayNormal():
    
    # prompt for the first point
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("First point")
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success: return
    point_a = gp.Point()
    
    # prompt for the second point
    gp.SetCommandPrompt("Second point")
    gp.SetBasePoint(point_a, True)
    gp.DrawLineFromPoint(point_a, True)
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success: return
    point_b = gp.Point()
    
    # tries to make a rectangle from 3 points
    def RectangleFrom3Points(a, b, c):
        
        plane = Rhino.Geometry.Plane(a, b, c)
        if not plane.IsValid: return
        
        width = a.DistanceTo(b)
        line = Rhino.Geometry.Line(a, b)
        height = line.DistanceTo(c, False)
        
        rect = Rhino.Geometry.Rectangle3d(plane, width, height)
        if rect: return rect
        
    # create dynamic display conduit to draw a rectangle
    def OnDynamicDraw(self, e):
        
        color = System.Drawing.Color.Red
        #color = scriptcontext.doc.Layers.CurrentLayer.Color
        
        # try to make a rectangle
        rect = RectangleFrom3Points(point_a, point_b, e.CurrentPoint)
        if not rect: return
        
        # display the rectangle and plane normal at rectangle center
        e.Display.DrawPolyline(rect.ToPolyline(), color, 2)
        e.Display.DrawDirectionArrow(rect.Center, rect.Plane.Normal, color)
        
    # prompt for the third point using dynamic display conduit
    gp.SetCommandPrompt("Third point")
    gp.EnableDrawLineFromPoint(False)
    gp.DynamicDraw += OnDynamicDraw
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success: return
    point_c = gp.Point()
    
    # try to add rectangle to document
    rect = RectangleFrom3Points(point_a, point_b, point_c)
    
    
    
    if rect: 
        return rect.Plane
    else:
        return
        
    #if rect.IsValid:
    #    scriptcontext.doc.Objects.AddRectangle(rect)
    #    scriptcontext.doc.Views.Redraw()
    
    # wash hands
    gp.Dispose()

DrawRectangleDisplayNormal()