# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import rhinoscriptsyntax as rs


class SimpleEtoDialog(forms.Dialog):
    def __init__(self):
        self.Title = "Sample Eto Dialog"
        self.ClientSize = drawing.Size(500, 300)
        self.Padding = drawing.Padding(5)
        self.Resizable = False

        text = forms.TextArea(Text="Lol")

        button = forms.Button(Tag=text)
        button.Text = "Click Me!"
        button.Click += self.OnPushPickButton

        layout = forms.DynamicLayout()
        layout.AddRow(text, button)
        self.Content = layout

    def OnPickPoint(self, sender, e):

        rs.GetPoints()

    def OnPushPickButton(self, sender, e):
        Rhino.UI.EtoExtensions.PushPickButton(self, self.OnPickPoint)
        button = sender
        name_box = button.Tag
        print(name_box.Text)


dialog = SimpleEtoDialog()
dialog.Show(Rhino.UI.RhinoEtoApp.MainWindow)
