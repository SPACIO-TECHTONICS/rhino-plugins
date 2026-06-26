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