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
import clr
import System  # type: ignore
clr.AddReference("Eto")
clr.AddReference("Rhino.UI")
from Eto import Forms, Drawing  # type: ignore
import Rhino  # type: ignore
import os
import scriptcontext as sc  # type: ignore

STICKY_KEY = "RhinoCharts_HUD_Instance"
PLUGIN_ID = "{cc7fb276-c476-4fb1-affb-52f4740fef4d}"

def get_hud_settings():
    """Retrieve the persistent settings for this plugin."""
    return Rhino.PlugIns.PlugIn.GetPluginSettings(System.Guid(PLUGIN_ID), False)

def save_hud_position(location):
    """Save the HUD location to Rhino's persistent settings."""
    try:
        settings = get_hud_settings()
        if settings:
            settings.SetInteger("HUD_X", int(location.X))
            settings.SetInteger("HUD_Y", int(location.Y))
    except Exception as e:
        Rhino.RhinoApp.WriteLine("RhinoCharts: Error saving HUD position: " + str(e))

def load_hud_position():
    """Load the last saved HUD location, or return None if not found."""
    try:
        settings = get_hud_settings()
        if settings and settings.ContainsKey("HUD_X") and settings.ContainsKey("HUD_Y"):
            x = settings.GetInteger("HUD_X")
            y = settings.GetInteger("HUD_Y")
            return Drawing.Point(x, y)
    except:
        pass
    return None

class ChartOverlay(Forms.Form):
    """A transparent, borderless floating window to act as a Viewport HUD."""
    
    # Private static reference for singleton behavior
    _overlay_instance = None
    
    @classmethod
    def instance(cls):
        # Prefer the sc.sticky reference to survive module reloads
        return sc.sticky.get(STICKY_KEY)
    
    def __init__(self):
        # Empty constructor for .NET compatibility
        pass

    def setup_ui(self, html_path, initial_data=None):
        try:
            Rhino.RhinoApp.WriteLine("RhinoCharts: Setting up Premium HUD Overlay...")
            self.Title = "RhinoCharts HUD"
            # Use getattr for "None" because it's a reserved keyword in Python
            self.WindowStyle = getattr(Forms.WindowStyle, "None") 
            self.Resizable = False 
            self.Topmost = True
            self.ShowInTaskbar = False
            
            # Transparency & Perfect Overlay Feel
            self.BackgroundColor = Drawing.Colors.Transparent
            self.Opacity = 1.0 # Keep at 1.0; fractional opacity can cause graying in IE11
            self.Owner = Rhino.UI.RhinoEtoApp.MainWindow
            self.Focusable = False # DO NOT STEAL FOCUS
            
            # Size and Position (Last saved or Bottom Right)
            self.ClientSize = Drawing.Size(420, 320)
            
            saved_pos = load_hud_position()
            if saved_pos:
                self.Location = saved_pos
            else:
                screen = Forms.Screen.PrimaryScreen.WorkingArea
                self.Location = Drawing.Point(screen.Width - 440, screen.Height - 360)
            
            # Layout Container (Must be transparent)
            layout = Forms.DynamicLayout()
            layout.BackgroundColor = Drawing.Colors.Transparent
            layout.Padding = Drawing.Padding(0)
            
            # Browser Control
            self.webview = Forms.WebView()
            self.webview.BackgroundColor = Drawing.Colors.Transparent
            layout.AddRow(self.webview)
            
            # Set the layout as the window content
            self.Content = layout
            
            # Load HUD mode
            uri_str = "file:///" + html_path.replace("\\", "/") + "?hud=true"
            Rhino.RhinoApp.WriteLine("RhinoCharts: Setting HUD URI: " + uri_str)
            self.webview.Url = System.Uri(uri_str)
            
            self.initial_data = initial_data
            self.webview.DocumentLoaded += self.on_loaded
            
            # Auto-close on any error to prevent zombie windows
            def on_web_error(s, e):
                Rhino.RhinoApp.WriteLine("RhinoCharts WEBVIEW ERROR: " + str(e))
            self.webview.Error += on_web_error
            
            # TITLE BRIDGE: For Closing and Moving
            self.webview.DocumentTitleChanged += self.on_title_changed
            
            Rhino.RhinoApp.WriteLine("RhinoCharts: HUD Initialization Complete.")
        except Exception as e:
            Rhino.RhinoApp.WriteLine("RhinoCharts FATAL ERROR in HUD setup: " + str(e))

    def on_title_changed(self, sender, e):
        title = self.webview.DocumentTitle
        if not title: return
        
        if title == "CLOSE":
            Rhino.RhinoApp.WriteLine("RhinoCharts: HUD Closing via UI signal...")
            self.Close()
            return
            
        if title.startswith("MOVE:"):
            try:
                # Format: MOVE:dx,dy|timestamp
                data = title.split(":")[1].split("|")[0]
                dx, dy = [float(val) for val in data.split(",")]
                self.Location = Drawing.Point(self.Location.X + dx, self.Location.Y + dy)
                save_hud_position(self.Location)
            except Exception as ex:
                pass # Throttled title changes might be malformed, just skip

    def on_loaded(self, sender, e):
        if self.initial_data:
            # Use UITimer instead of Thread.Sleep to avoid blocking the UI thread
            self.timer = Forms.UITimer(Interval=0.3)
            self.timer.Elapsed += self.on_timer_elapsed
            self.timer.Start()

    def on_timer_elapsed(self, sender, e):
        self.timer.Stop()
        if self.initial_data:
            self.update_data(self.initial_data)

    def update_data(self, json_data):
        if not self.webview: return
        # Ensure we call the global bridge function
        script = "if(window.updateChart) { window.updateChart(" + json_data + "); }"
        self.webview.ExecuteScript(script)

    @classmethod
    def show_or_update(cls, html_path, json_data):
        """Create or update the singleton overlay instance."""
        try:
            # Check scriptcontext.sticky for persistence across module reloads
            instance = sc.sticky.get(STICKY_KEY)
            
            if instance is None:
                Rhino.RhinoApp.WriteLine("RhinoCharts: Launching New HUD persistence layer...")
                new_instance = cls()
                new_instance.setup_ui(html_path, json_data)
                
                # Store in sticky for cross-reload access
                sc.sticky[STICKY_KEY] = new_instance
                
                # Reset singleton when closed
                def on_closed(s, e):
                    if STICKY_KEY in sc.sticky:
                        del sc.sticky[STICKY_KEY]
                    Rhino.RhinoApp.WriteLine("RhinoCharts: HUD Window Closed.")
                new_instance.Closed += on_closed
                
                new_instance.Show()
                Rhino.RhinoApp.WriteLine("RhinoCharts: HUD .Show() executed.")
                return new_instance
            else:
                # Existing HUD found in sticky
                try:
                    instance.BringToFront()
                    instance.update_data(json_data)
                except Exception as e:
                    # If the instance is dead or invalid, recreate it
                    Rhino.RhinoApp.WriteLine("RhinoCharts: Existing HUD invalid, recreating: " + str(e))
                    if STICKY_KEY in sc.sticky: del sc.sticky[STICKY_KEY]
                    return cls.show_or_update(html_path, json_data)
                return instance
        except Exception as ex:
            Rhino.RhinoApp.WriteLine("RhinoCharts ERROR: Failed to show HUD: {}".format(ex))
            return None

    @classmethod
    def close_instance(cls):
        instance = sc.sticky.get(STICKY_KEY)
        if instance:
            try:
                instance.Close()
            except:
                pass
            if STICKY_KEY in sc.sticky:
                del sc.sticky[STICKY_KEY]

    def OnClosed(self, e):
        # Save final position on close
        save_hud_position(self.Location)
        # Clean up the sticky reference when window is closed
        if STICKY_KEY in sc.sticky:
            del sc.sticky[STICKY_KEY]
