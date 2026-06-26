# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

"""Sorts selected objects by their bounding box centers along X, Y, or Z axes, and stores the sorted list in memory for knDistributeonCurve."""

import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "knSortSelection"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    objects = rs.GetObjects("Select objects to sort", preselect=True)
    if not objects: return 1
    
    default_sort = "X_LeftToRight"
    if sc.sticky.has_key("knSortSelection_LastSort"):
        default_sort = sc.sticky["knSortSelection_LastSort"]
        
    options = [
        "X_LeftToRight", "X_RightToLeft", 
        "Y_BottomToTop", "Y_TopToBottom", 
        "Z_LowToHigh", "Z_HighToLow"
    ]
    
    sort_method = rs.GetString("Sort direction based on object centers", default_sort, options)
    if not sort_method: return 1
    
    sc.sticky["knSortSelection_LastSort"] = sort_method
    
    sortable_list = []
    
    for obj in objects:
        bbox = rs.BoundingBox(obj)
        if not bbox: continue
        
        cx = (bbox[0].X + bbox[2].X) / 2.0
        cy = (bbox[0].Y + bbox[2].Y) / 2.0
        cz = (bbox[0].Z + bbox[4].Z) / 2.0
        
        if sort_method == "X_LeftToRight": val = cx
        elif sort_method == "X_RightToLeft": val = -cx
        elif sort_method == "Y_BottomToTop": val = cy
        elif sort_method == "Y_TopToBottom": val = -cy
        elif sort_method == "Z_LowToHigh": val = cz
        elif sort_method == "Z_HighToLow": val = -cz
        else: val = cx
        
        sortable_list.append((val, obj))
        
    sortable_list.sort(key=lambda x: x[0])
    
    sorted_objects = [item[1] for item in sortable_list]
    
    sc.sticky["knDistributeonCurve_LastObjects"] = sorted_objects
    
    rs.UnselectAllObjects()
    rs.SelectObjects(sorted_objects)
    
    print "Successfully sorted {} objects by {}. Ready for knDistributeonCurve!".format(len(sorted_objects), sort_method)
    
    return 0

RunCommand(True)