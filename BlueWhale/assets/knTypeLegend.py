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

import Rhino  # type: ignore
import System.Drawing  # type: ignore
import scriptcontext  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
 
# DisplayConduit subclass that overrides the DrawForeground function
# e is an instance of Rhino.Display.DrawEventArgs
class CustomConduit(Rhino.Display.DisplayConduit):
    def DrawForeground(self, e):
        color = System.Drawing.Color.Red
        bounds = e.Viewport.Bounds
        pt = Rhino.Geometry.Point2d(bounds.Right - 100, bounds.Bottom - 30)
        e.Display.Draw2dText("Hello", color, pt, False)
        
        col = System.Drawing.Color.Blue
        rectangle = System.Drawing.Rectangle(50,100,100,100)
        e.Display.Draw2dRectangle(rectangle,color,10,col)
    

     

 
 
def showafterscript():
    # Create a custom conduit that can continue to draw after the
    # script has completed. The conduit is kept in the sticky
    # dictionary so we can get at it and turn it off in the future
    #
    # check to see if the conduit has been created and is in sticky
    conduit = None
    if scriptcontext.sticky.has_key("myconduit"):
        conduit = scriptcontext.sticky["myconduit"]
    else:
        # create a conduit and place it in sticky
        conduit = CustomConduit()
        scriptcontext.sticky["myconduit"] = conduit
 
    # Toggle enabled state for conduit. Every time this script is
    # run, it will turn the conduit on and off
    conduit.Enabled = not conduit.Enabled
    if conduit.Enabled: print("conduit enabled")
    else: print("conduit disabled")
    scriptcontext.doc.Views.Redraw()
 
 
def showinscript():
    # create a custom conduit that only displays during the execution
    # of this script. Once the script has completed, the conduit is turned
    # off and display goes back to normal
    conduit = CustomConduit()
    conduit.Enabled = True
    scriptcontext.doc.Views.Redraw()
    rs.GetString("Pausing for user input")
    conduit.Enabled = False
    scriptcontext.doc.Views.Redraw()
 
if __name__=="__main__":
    showinscript()
    #showafterscript()