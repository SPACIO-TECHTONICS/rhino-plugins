from __future__ import print_function
import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore
from Rhino.Commands import *  # type: ignore
from Rhino.DocObjects import *  # type: ignore
from Rhino.Input import *  # type: ignore

__commandname__ = "knAddDetailNameBlock"

# RunCommand is called when the user enters the command name in Rhino.
def RunCommand(is_interactive):


detailnumber = 1
    pageview = sc.doc.Views.ActiveView
    
    if type(pageview) != Rhino.Display.RhinoPageView:
        rs.MessageBox("This tool only works in layout space.")
        return
    
    details = rs.GetObjects("Select detail(s) to name", 32768, preselect=True)
    if not details:
        return
    
    for detail in details:
        detailobj = rs.coercerhinoobject(detail)
        
        if detailobj.Name:
            add_detail_scale(detail, detailnumber, pageview.PageName)
        else:
            rs.SelectObject(detail)
            name = rs.StringBox("Enter the name of the selected detail")
            # Proceed only if the user didn't hit cancel
            if name:
                rs.ObjectName(detail, name)
                add_detail_scale(detail, detailnumber, pageview.PageName)
            
            rs.UnselectAllObjects()
            
        detailnumber += 1
    return

def add_detail_scale(detail_guid, number, pagename):
    # Set focus back to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    
    detail = rs.coercerhinoobject(detail_guid)
    detail_name = detail.Name if detail.Name else "Detail"
    
    # --- PLACEMENT LOGIC WITH MEMORY ---
    base_pt = None
    sticky_key = "kn_LastDetailPoint"
    
    # Check if we have a saved point from a previous run
    if sc.sticky.has_key(sticky_key):
        last_pt = sc.sticky[sticky_key]
        ans = rs.GetString("Use previous location for " + detail_name + "?", "Yes", ["Yes", "No"])
        
        if ans and ans.lower() in ["yes", "y"]:
            base_pt = last_pt
            
    # If no saved point or user chose "No", prompt for a new point
    if not base_pt:
        rs.SelectObject(detail_guid)
        base_pt = rs.GetPoint("Pick location for detail bubble (circle center) for: " + detail_name)
        rs.UnselectObject(detail_guid)
        
        if not base_pt:
            print("Placement cancelled for " + detail_name)
            return
            
        # Save this new point to sticky memory for next time
        sc.sticky[sticky_key] = base_pt

    # --- GET CURRENT DIMENSION STYLE SETTINGS ---
    current_dimstyle = sc.doc.DimStyles.Current
    h = current_dimstyle.TextHeight
    font_name = current_dimstyle.Font.FamilyName
    
    # Fallback just in case text height in the style is set to 0
    if h <= 0:
        h = 1.0 
    
    if detail.DetailGeometry.IsParallelProjection:
        # Calculate text points relative to user-selected base point (base_pt = pt3 / center of circle)
        pt3 = base_pt
        
        # Scale text (top left justification, goes below the line)
        pt1 = [base_pt.X + (3 * h), base_pt.Y - h, base_pt.Z]
        
        # Name text (bottom left justification, goes above the line)
        pt2 = [base_pt.X + (3 * h), base_pt.Y + h, base_pt.Z]
        
        detail_id_str = str(detail.Id)
        
        # --- UNIT SYSTEM HANDLING ---
        # 8 = Inches, 9 = Feet
        unit_sys = rs.UnitSystem()
        if unit_sys == 8 or unit_sys == 9:
            scale_format = "'#=1-0'" # Imperial Architectural
        else:
            scale_format = "'1:#'"   # Metric Ratio
            
        scale = "%<DetailScale('" + detail_id_str + "'," + scale_format + ")>%"
        name = "%<ObjectName('" + detail_id_str + "')>%"
        
        sc.doc.Views.ActiveView = pageview
        
        # 1. Add Text first so we can measure it
        name_id = rs.AddText(name, pt2, h, font=font_name, font_style=1, justification=65537) # bottom left
        scale_id = rs.AddText(scale, pt1, h, font=font_name, justification=262145) # top left
        number_id = rs.AddText(str(number), pt3, h, font=font_name, justification=131074) # middle center
        
        # 2. Calculate line length based on text bounding boxes
        text_start_x = base_pt.X + (3 * h)
        max_text_x = text_start_x
        
        name_bbox = rs.BoundingBox(name_id)
        if name_bbox:
            max_text_x = max(max_text_x, max([pt.X for pt in name_bbox]))
            
        scale_bbox = rs.BoundingBox(scale_id)
        if scale_bbox:
            max_text_x = max(max_text_x, max([pt.X for pt in scale_bbox]))
            
        # Find exact length of the text block and add 10%
        text_length = max_text_x - text_start_x
        if text_length < 0: text_length = 0
        extension = text_length * 0.10
            
        # 3. Define line start and end points
        pt4 = [base_pt.X + h, base_pt.Y, base_pt.Z]
        pt5 = [max_text_x + extension, base_pt.Y, base_pt.Z]
        
        # 4. Draw Circle and Line
        circle_id = rs.AddCircle(pt3, 2 * h)
        line_id = rs.AddLine(pt4, pt5)
        
        # Group everything together including the detail view
        ids = [name_id, scale_id, circle_id, line_id, detail_guid, number_id]
        ids = [i for i in ids if i]
        if ids:
            groupind = sc.doc.Groups.Add(ids)

        # --- LOCK THE DETAIL VIEW ---
        detail.DetailGeometry.IsProjectionLocked = True
        detail.CommitChanges()

if __name__ == "__main__":
    RunCommand(True)
