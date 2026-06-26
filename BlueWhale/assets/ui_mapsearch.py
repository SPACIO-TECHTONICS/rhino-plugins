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

# -*- coding: utf-8 -*-
import Rhino.UI  # type: ignore
import Eto.Drawing as drawing  # type: ignore
import Eto.Forms as forms  # type: ignore
import os
import System  # type: ignore

class MapBBoxDialog(forms.Dialog):
    def __init__(self):
        self.bbox_result = None
        
        self.Title = "Select Area on Map"
        self.ClientSize = drawing.Size(800, 600)
        self.Resizable = True
        
        # WebView
        self.web_view = forms.WebView()
        
        # Load HTML content
        curr_dir = os.path.dirname(__file__)
        html_path = os.path.join(curr_dir, "map_selector.html")
        
        with open(html_path, 'r') as f:
            html_content = f.read()
            
        # We use a dummy base URL to allow relative references if needed
        # but here we load direct content.
        self.web_view.LoadHtml(html_content)
        
        # Listen for coordinate selection via DocumentTitle
        self.web_view.DocumentTitleChanged += self.on_title_changed
        
        # Layout
        layout = forms.DynamicLayout()
        layout.AddRow(self.web_view)
        self.Content = layout

    def on_title_changed(self, sender, e):
        title = self.web_view.DocumentTitle
        if title and title.startswith("BBOX:"):
            # Format: BBOX:lat,lon,lat,lon
            self.bbox_result = title.replace("BBOX:", "")
            self.Close()

def show_map_selector():
    """
    Shows the interactive map selector and returns the BBox string.
    Returns: "min_lat,min_lon,max_lat,max_lon" or None
    """
    dialog = MapBBoxDialog()
    dialog.Owner = Rhino.UI.RhinoEtoApp.MainWindow
    dialog.ShowModal()
    
    return dialog.bbox_result
