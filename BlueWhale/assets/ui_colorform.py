# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import rhinoscriptsyntax as rs
import random
import scriptcontext as sc
import osm_utilities as osm


class ColorForm(forms.Dialog):
    def __init__(self, title, keys, values):
        self.Title = title
        self.ClientSize = drawing.Size(500, 300)
        self.controls = {}
        self.counter = len(keys)
        self.new_rows = {}

        for i in range(len(keys)):
            name_box = forms.TextBox(Text=keys[i])
            color_box = forms.TextBox(Text=values[i])
            button = forms.Button(Text="Color", Tag=(color_box, name_box))
            remove_button = forms.Button(Text="Remove Type")
            addobjects_button = forms.Button(Text="+", Tag=(color_box, name_box))
            button.Click += self.button_Click
            remove_button.Click += self.remove_row_Click
            addobjects_button.Click += self.OnPushPickButton
            self.controls[keys[i]] = (name_box, color_box, button, remove_button,addobjects_button)

        self.button = forms.Button()
        self.button.Text = "Submit"
        self.button.Click += self.submit_Click

        self.add_row_button = forms.Button()
        self.add_row_button.Text = "Add Type"
        self.add_row_button.Click += self.add_row_Click
        
        self.viz_button = forms.Button()
        self.viz_button.Text = "Display in 3d"
        self.viz_button.Click += self.vizButton_Click

        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        for key in keys:
            name_box, text_box, button, remove_button,addobjects_button = self.controls[key]
            layout.AddRow(name_box, text_box, button, remove_button,addobjects_button)

        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button,self.viz_button)

        self.Content = layout
        
    def OnPushPickButton(self, sender, e):
        button = sender
        color_box, name_box = button.Tag
    
        Rhino.UI.EtoExtensions.PushPickButton(self, lambda s, a: self.AddByPicking(name_box))
    
    def AddByPicking(self, name_box):
        text = name_box.Text
        prompt = "Select objects to be assigned {} type".format(text)
        objs = rs.GetObjects(prompt)
        if objs:
            for obj in objs:
                rs.SetUserText(obj, "URBAN3D::Type", text)
        else:
            rs.MessageBox("Objects not assigned since the command was canceled")



            
            
    def button_Click(self, sender, e):
        button = sender
        text_box, name_box = button.Tag

        old_text = text_box.Text
        result = rs.GetColor()
        result = str(result[0])+','+str(result[1])+','+str(result[2])
        

        if result is not None:
            color = result
            text_box.Text = str(color)
        else:
            text_box.Text = old_text


    def submit_Click(self, sender, e):
        button = sender
        values = {}
        names = {}

        for key, (name_box, box, _, _) in self.controls.items():
            values[key] = box.Text
            names[key] = name_box.Text

        names[None] = None
        values[None] = None
        
        self.Tag = (names, values, self.new_rows)
        self.Close()

    def add_row_Click(self, sender, e):
        self.counter += 1
        new_key = "Color{}".format(self.counter)
        new_value = self.generate_pastel_color()
    
        name_box = forms.TextBox(Text=new_key)
        color_box = forms.TextBox(Text=new_value)
        button = forms.Button(Text="Color", Tag=(color_box, name_box))
        remove_button = forms.Button(Text="Remove Type")
        addobjects_button = forms.Button(Text="+", Tag=(color_box, name_box))
        button.Click += self.button_Click
        remove_button.Click += self.remove_row_Click
        addobjects_button.Click += self.OnPushPickButton
        self.controls[new_key] = (name_box, color_box, button, remove_button, addobjects_button)
    
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)
    
        for key in self.controls:
            name_box, text_box, button, remove_button, addobjects_button = self.controls[key]
            layout.AddRow(name_box, text_box, button, remove_button, addobjects_button)
    
        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button)
    
        scrollable_layout = forms.Scrollable()
        scrollable_layout.Content = layout
        scrollable_layout.Border = forms.BorderType.None
    
        scrollable_layout.Height += 100
    
        self.Content = scrollable_layout

        

    def remove_row_Click(self, sender, e):
        remove_button = sender

        for key, (name_box, color_box, button, remove_btn,addobjects_button) in self.controls.items():
            if remove_button is remove_btn:
                del self.controls[key]
                break
        
        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        for key in self.controls:
            name_box, text_box, button, remove_button,addobjects_button = self.controls[key]
            layout.AddRow(name_box, text_box, button, remove_button,addobjects_button)

        layout.AddRow(None)
        layout.AddRow(self.add_row_button, self.button)

        scrollable_layout = forms.Scrollable()
        scrollable_layout.Content = layout
        scrollable_layout.Border = forms.BorderType.None

        scrollable_layout.Height += 100

        self.Content = scrollable_layout
        
    def generate_pastel_color(self):
        r = random.randint(64, 223)
        g = random.randint(64, 223)
        b = random.randint(64, 223)
        
        return "{}, {}, {}".format(r, g, b)
    
    def vizButton_Click(self, sender, e):
        objs = rs.NormalObjects()
        for obj in objs:
            keys = rs.GetUserText(obj)
            if keys:
                for key in keys:
                    type = rs.GetUserText(obj, "URBAN3d::Type")
                    if type:
                        color = rs.GetDocumentUserText("URBAN3d::Type::{}".format(type))
                        color = tuple(int(x) for x in color.split(',') if x.isdigit())
                        rs.ObjectColor(obj,osm.tuple_to_color(color))
    
    
        


def show_eto_form_with_colors(title, keys, values):
    dialog = ColorForm(title, keys, values)
    
    dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    
    if dialog.Tag:
        _,values,_= dialog.Tag
        return values
    else:
        return

    

keys = ["Color1", "Color2", "Color3","lol"]
values = ["255, 0, 0", "0, 255, 0", "0, 0, 255","0,0,0"]

result = show_eto_form_with_colors("Color Form", keys, values)

print(result)