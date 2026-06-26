from __future__ import print_function
import Rhino  # type: ignore
import System.Drawing  # type: ignore

class ChartDisplayConduit(Rhino.Display.DisplayConduit):
    def __init__(self):
        self.bitmap = None
        self._display_bitmap = None
        
    def update_image(self, bitmap):
        """Update the conduit with a new bitmap image"""
        print("RhinoCharts: Updating conduit image...")
        try:
            # Dispose old resources
            if self._display_bitmap:
                self._display_bitmap.Dispose()
            if self.bitmap:
                self.bitmap.Dispose()
                
            self.bitmap = bitmap
            # Create a Rhino DisplayBitmap from the System.Drawing.Bitmap
            self._display_bitmap = Rhino.Display.DisplayBitmap(self.bitmap)
            
            # Ensure conduit is enabled and redraw
            self.Enabled = True
            Rhino.RhinoDoc.ActiveDoc.Views.Redraw()
        except Exception as ex:
            Rhino.RhinoApp.WriteLine("RhinoCharts Conduit Error: {}".format(ex))

    def DrawForeground(self, e):
        if not self._display_bitmap:
            return
            
        # print("RhinoCharts: DrawForeground active") # Commented out to avoid spamming the console
        # Get viewport dimensions
        bounds = e.Viewport.Bounds
        view_w = bounds.Width
        view_h = bounds.Height
        
        # Image dimensions
        img_w = self.bitmap.Width
        img_h = self.bitmap.Height
        
        # Position: Bottom Right with margin
        margin = 15
        x = view_w - img_w - margin
        y = view_h - img_h - margin
        
        # Draw a subtle dark background behind the chart for contrast
        # Note: We use screen coordinates in DrawForeground
        rect = System.Drawing.Rectangle(x - 5, y - 5, img_w + 10, img_h + 10)
        e.Display.DrawFillPaddingRect(rect, System.Drawing.Color.FromArgb(120, 20, 20, 20))
        
        # Draw the bitmap
        e.Display.DrawBitmap(self._display_bitmap, x, y)

    def clear(self):
        """Disable conduit and free resources"""
        print("RhinoCharts: Clearing conduit...")
        self.Enabled = False
        if self._display_bitmap:
            self._display_bitmap.Dispose()
            self._display_bitmap = None
        if self.bitmap:
            self.bitmap.Dispose()
            self.bitmap = None
        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()
