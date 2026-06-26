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

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import Eto.Forms as forms
import Eto.Drawing as drawing

__commandname__ = "knSelBlock"

class BlockSearchDialog(forms.Dialog[bool]):
    def __init__(self):
        self.Title = "knSelBlock - Search and Select"
        self.ClientSize = drawing.Size(350, 400)
        self.Padding = drawing.Padding(12)
        
        self.selected_blocks = []
        
        # --- UI Controls ---
        self.lbl_search = forms.Label(Text="Type at least 3 characters to search:")
        self.txt_search = forms.TextBox()
        self.txt_search.TextChanged += self.OnSearchTextChanged
        
        # GridView handles high-performance vertical layout tracking seamlessly
        self.grid_blocks = forms.GridView()
        self.grid_blocks.ShowHeader = False
        self.grid_blocks.AllowMultipleSelection = True
        
        column = forms.GridColumn()
        column.DataCell = forms.TextBoxCell(0)
        column.Editable = False
        self.grid_blocks.Columns.Add(column)
        
        self.btn_select_all = forms.Button(Text="Select All Matches")
        self.btn_select_all.Click += self.OnCheckAllMatches
        
        self.btn_ok = forms.Button(Text="Select Blocks in Model")
        self.btn_ok.Click += self.OnOkClick
        
        self.btn_cancel = forms.Button(Text="Cancel")
        self.btn_cancel.Click += self.OnCancelClick
        
        # --- Layout Assembly ---
        layout = forms.TableLayout()
        layout.Spacing = drawing.Size(6, 6)
        
        scrollable = forms.Scrollable()
        scrollable.Content = self.grid_blocks
        scrollable_row = forms.TableRow(scrollable)
        scrollable_row.ScaleHeight = True 
        
        footer_layout = forms.TableLayout()
        footer_layout.Spacing = drawing.Size(6, 6)
        footer_layout.Rows.Add(forms.TableRow(None, self.btn_ok, self.btn_cancel))
        
        # Assembled cleanly without the viewport picker button layout track
        layout.Rows.Add(forms.TableRow(self.lbl_search))
        layout.Rows.Add(forms.TableRow(self.txt_search))
        layout.Rows.Add(scrollable_row) 
        layout.Rows.Add(forms.TableRow(self.btn_select_all))
        layout.Rows.Add(forms.TableRow(forms.Label()))
        layout.Rows.Add(forms.TableRow(footer_layout))
        
        self.Content = layout

    def PopulateList(self, items):
        self.grid_blocks.DataStore = [(item,) for item in items]

    def OnSearchTextChanged(self, sender, e):
        search_term = self.txt_search.Text.lower().strip()
        
        if len(search_term) < 3:
            self.PopulateList([])
            self.lbl_search.Text = "Type at least 3 characters to search..."
            return
            
        self.lbl_search.Text = "Searching..."
        
        all_blocks = rs.BlockNames()
        if not all_blocks:
            return
            
        filtered = [name for name in all_blocks if search_term in name.lower()]
        
        self.PopulateList(sorted(filtered))
        self.lbl_search.Text = "Found {} matching blocks:".format(len(filtered))

    def OnCheckAllMatches(self, sender, e):
        if self.grid_blocks.DataStore:
            all_indices = range(len(list(self.grid_blocks.DataStore)))
            self.grid_blocks.SelectedRows = all_indices

    def OnOkClick(self, sender, e):
        self.selected_blocks = []
        if self.grid_blocks.SelectedItems:
            for item in self.grid_blocks.SelectedItems:
                if item and isinstance(item, tuple):
                    self.selected_blocks.append(item[0])
        self.Close(True)

    def OnCancelClick(self, sender, e):
        self.Close(False)


def RunCommand( is_interactive ):
    matching_blocks = []
    
    # 1. Pre-selection bypass check
    pre_selected = rs.SelectedObjects()
    if pre_selected:
        for obj in pre_selected:
            if rs.IsBlockInstance(obj):
                b_name = rs.BlockInstanceName(obj)
                if b_name and b_name not in matching_blocks:
                    matching_blocks.append(b_name)
                    
    # 2. Launch cleaner form if nothing was selected beforehand
    if not matching_blocks:
        dialog = BlockSearchDialog()
        rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
        if rc and dialog.selected_blocks:
            matching_blocks = dialog.selected_blocks
        else:
            return 1

    # 3. Compile and apply selection stack
    if matching_blocks:
        objects_to_select = []
        
        rs.EnableRedraw(False)
        
        for block in matching_blocks:
            instances = rs.BlockInstances(block)
            if instances:
                objects_to_select.extend(instances)
                
        if objects_to_select:
            rs.UnselectAllObjects()
            rs.SelectObjects(objects_to_select)
            
            rs.EnableRedraw(True)
            scriptcontext.doc.Views.Redraw()
            print "Selected {} instances across blocks: {}.".format(len(objects_to_select), ", ".join(matching_blocks))
        else:
            rs.EnableRedraw(True)
            print "Selected blocks exist, but no active instances are visible in the model space."
            
    return 0

if __name__ == "__main__":
    RunCommand(True)