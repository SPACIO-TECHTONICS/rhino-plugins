# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms


class NumberForm(forms.Dialog):
    def __init__(self, title, *titles):
        self.Title = title
        self.ClientSize = drawing.Size(300, 200)

        self.number_boxes = {}

        for title in titles:
            number_box = forms.NumericUpDown()
            self.number_boxes[title] = number_box

        self.button = forms.Button()
        self.button.Text = "Submit"
        self.button.Click += self.button_Click

        layout = forms.DynamicLayout()
        layout.DefaultSpacing = drawing.Size(5, 5)
        layout.Padding = drawing.Padding(10)

        for title in titles:
            layout.AddRow(forms.Label(Text=title), self.number_boxes[title])

        layout.AddRow(None)
        layout.AddRow(self.button)

        self.Content = layout

    def button_Click(self, sender, e):
        values = {}

        for title in self.number_boxes:
            value = self.number_boxes[title].Value
            values[title] = value

        self.Tag = values
        self.Close()


def show_eto_form_with_titles(*titles):
    dialog = NumberForm(*titles)

    dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)

    return dialog.Tag
