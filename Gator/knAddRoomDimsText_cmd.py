# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import Rhino
import System.Drawing

DETAIL_KEY = "KN_LAST_DETAIL_ID"

def format_arch(dist, u_sys):
    dist = float(dist)
    if u_sys == Rhino.UnitSystem.Feet:
        total_inches = dist * 12.0
    else:
        total_inches = dist
    
    feet = int(total_inches // 12)
    inches = int(round(total_inches % 12))
    if inches == 12:
        feet += 1
        inches = 0
    return "{0}' - {1}\"".format(feet, inches)

def RunCommand(is_interactive):


    sc.doc = Rhino.RhinoDoc.ActiveDoc
    u_sys = sc.doc.ModelUnitSystem
    
    detail_id = None
    all_details = rs.ObjectsByType(rs.filter.detail)
    
    if not all_details:
        print("No details found on this layout.")
        return
    
    if len(all_details) == 1:
        detail_id = all_details[0]
    else:
        prev_detail = sc.sticky.get(DETAIL_KEY)
        if prev_detail and rs.IsObject(prev_detail):
            choice = rs.GetString("Use previous detail?", "Yes", ["Yes", "SelectNew"])
            if choice == "SelectNew":
                detail_id = rs.GetObject("Select the Detail View", rs.filter.detail)
            else:
                detail_id = prev_detail
        else:
            detail_id = rs.GetObject("Select the Detail View", rs.filter.detail)

    if not detail_id: return
    sc.sticky[DETAIL_KEY] = detail_id
    
    detail_obj = rs.coercegeometry(detail_id)
    scale = detail_obj.PageToModelRatio
    if scale == 0: scale = 1.0

    l_pts = rs.GetLine(0, message1="Length Start", message2="Length End")
    if not l_pts: return
    w_pts = rs.GetLine(0, message1="Width Start", message2="Width End")
    if not w_pts: return

    real_len = l_pts[0].DistanceTo(l_pts[1]) / scale
    real_wid = w_pts[0].DistanceTo(w_pts[1]) / scale
    
    dim_str = "{} x {}".format(format_arch(real_len, u_sys), format_arch(real_wid, u_sys))

    def GetPointDynamic(sender, args):
        plane = rg.Plane.WorldXY
        plane.Origin = args.CurrentPoint
        temp_text = rg.TextEntity.Create(dim_str, plane, sc.doc.DimStyles.Current, False, 0, 0)
        temp_text.Justification = rg.TextJustification.MiddleCenter
        args.Display.DrawText(temp_text, System.Drawing.Color.Black)

    gp = Rhino.Input.Custom.GetPoint()
    gp.DynamicDraw += GetPointDynamic
    gp.Get()
    
    if gp.CommandResult() != Rhino.Commands.Result.Success: return
    
    final_plane = rg.Plane.WorldXY
    final_plane.Origin = gp.Point()
    text_ent = rg.TextEntity.Create(dim_str, final_plane, sc.doc.DimStyles.Current, False, 0, 0)
    text_ent.Justification = rg.TextJustification.MiddleCenter
    
    sc.doc.Objects.AddText(text_ent)
    sc.doc.Views.Redraw()

if __name__ == "__main__":
    RunCommand(True)
