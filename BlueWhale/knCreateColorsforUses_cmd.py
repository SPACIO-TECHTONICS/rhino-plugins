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

import Rhino.UI  # type: ignore
import Eto.Drawing as drawing  # type: ignore
import Eto.Forms as forms  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore
import random
import scriptcontext as sc  # type: ignore
import Rhino  # type: ignore
from assets import osm_utilities as osm
from assets import auth_helper

__commandname__ = "knCreateColorsforUses"

class ColorForm(forms.Form):
    def __init__(self):
        self.title = None
        self.keys = None
        self.values = None
        self.counter = 0
        self.controls = {}
        self.new_rows = {}
        
        self.ClientSize = drawing.Size(500, 300)
        self.Title = "Use Color Manager"

        self.button = forms.Button()
        self.button.Text = "Submit"
        self.button.Click += self.submit_Click

        self.add_row_button = forms.Button()
        self.add_row_button.Text = "Add Type"
        self.add_row_button.Click += self.add_row_Click
        
        self.viz_button = forms.Button()
        self.viz_button.Text = "Display in 3D"
        self.viz_button.Click += self.vizButton_Click

        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button, self.viz_button)

        self.Content = layout
        
    def show_dialog(self, title, keys, values):
        self.title = title
        self.keys = keys
        self.values = values
        self.counter = len(keys)
        
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        for i in range(len(keys)):
            name_box = forms.TextBox(Text=keys[i])
            button = forms.Button(Tag=name_box)
            
            try:
                rgb_parts = [int(x) for x in values[i].split(",")]
                button.BackgroundColor = drawing.Color.FromArgb(rgb_parts[0], rgb_parts[1], rgb_parts[2])
            except:
                button.BackgroundColor = drawing.Color.FromArgb(200, 200, 200)
            
            remove_button = forms.Button(Text="Remove")
            add_objs_button = forms.Button(Text="+", Tag=name_box)
            
            button.Click += self.button_Click
            remove_button.Click += self.remove_row_Click
            add_objs_button.Click += self.OnPushPickButton
            
            self.controls[keys[i]] = (name_box, button, remove_button, add_objs_button)
            layout.AddRow(name_box, button, remove_button, add_objs_button)
            
        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button, self.viz_button)
        
        scrollable = forms.Scrollable()
        scrollable.Content = layout
        self.Content = scrollable
        self.Title = title
        
        self.Owner = Rhino.UI.RhinoEtoApp.MainWindow
        self.Show()
    
    def OnClosing(self, e):
        self.submit_Click(None, None)
        super(ColorForm, self).OnClosing(e)
        
    def OnPushPickButton(self, sender, e):
        name_box = sender.Tag
        Rhino.UI.EtoExtensions.PushPickButton(self, lambda s, a: self.AddByPicking(name_box))
    
    def AddByPicking(self, name_box):
        text = name_box.Text
        objs = rs.GetObjects("Select objects to assign type: {0}".format(text))
        if objs:
            for obj in objs:
                rs.SetUserText(obj, "URBAN3D::Type", text)
        else:
            print("Selection canceled.")

    def button_Click(self, sender, e):
        res = rs.GetColor()
        if res is not None:
            sender.BackgroundColor = drawing.Color.FromArgb(res[0], res[1], res[2])

    def submit_Click(self, sender, e):
        results = {}
        for key in self.controls:
            ctrls = self.controls[key]
            name = ctrls[0].Text
            color = ctrls[1].BackgroundColor
            rgb_str = "{0}, {1}, {2}".format(int(color.R * 255), int(color.G * 255), int(color.B * 255))
            results["URBAN3D::Type::{0}".format(name)] = rgb_str
            
        osm.ClearDocumentTextswithSubstring("URBAN3D::Type::")
        osm.StoreasDocumentUserText(results)

    def add_row_Click(self, sender, e):
        self.counter += 1
        new_key = "Type_{0}".format(self.counter)
        
        name_box = forms.TextBox(Text=new_key)
        button = forms.Button(Tag=name_box)
        
        p_color = self.generate_pastel_color()
        rgb = [int(x) for x in p_color.split(",")]
        button.BackgroundColor = drawing.Color.FromArgb(rgb[0], rgb[1], rgb[2])
        
        remove_button = forms.Button(Text="Remove")
        add_objs_button = forms.Button(Text="+", Tag=name_box)
        
        button.Click += self.button_Click
        remove_button.Click += self.remove_row_Click
        add_objs_button.Click += self.OnPushPickButton
        
        self.controls[new_key] = (name_box, button, remove_button, add_objs_button)
        self.refresh_layout()

    def remove_row_Click(self, sender, e):
        target_key = None
        for key, ctrls in self.controls.items():
            if ctrls[2] is sender:
                target_key = key
                break
        if target_key:
            del self.controls[target_key]
            self.refresh_layout()

    def refresh_layout(self):
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)
        
        for key in self.controls:
            ctrls = self.controls[key]
            layout.AddRow(ctrls[0], ctrls[1], ctrls[2], ctrls[3])
            
        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button, self.viz_button)
        
        scrollable = forms.Scrollable()
        scrollable.Content = layout
        self.Content = scrollable

    def generate_pastel_color(self):
        r = random.randint(64, 223)
        g = random.randint(64, 223)
        b = random.randint(64, 223)
        return "{0}, {1}, {2}".format(r, g, b)

    def vizButton_Click(self, sender, e):
        objs = rs.AllObjects()
        rs.EnableRedraw(False)
        for obj in objs:
            u_type = rs.GetUserText(obj, "URBAN3D::Type")
            if u_type:
                color_str = rs.GetDocumentUserText("URBAN3D::Type::{0}".format(u_type))
                if color_str:
                    try:
                        color = tuple(int(x) for x in color_str.split(',') if x.strip().isdigit())
                        if len(color) == 3:
                            rs.ObjectColor(obj, osm.tuple_to_color(color))
                    except:
                        pass
        rs.EnableRedraw(True)

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knCreateColorsforUses"):
        return auth_helper.get_cancel_result()

    keys = []
    values = []
    
    doc_text = rs.GetDocumentUserText()
    matches = osm.StringswithSubstring("URBAN3D::Type::", doc_text)
    
    if matches:
        for s in matches:
            keys.append(s.replace("URBAN3D::Type::", ""))
            values.append(rs.GetDocumentUserText(s))
        
        form = ColorForm()
        form.show_dialog("Use Color Manager", keys, values)
        return Rhino.Commands.Result.Success
    else:
        osm.StoreasDocumentUserText(osm.colorsDict)
        rs.MessageBox("Initialized types with default colors. Please run the command again to manage them.")
        return Rhino.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
