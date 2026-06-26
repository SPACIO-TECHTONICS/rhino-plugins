# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import scriptcontext as sc

__commandname__ = "knCenterDivideCurve"

def RunCommand( is_interactive ):


    print("Executing " + __commandname__)
    
    curve_info = rs.GetCurveObject("Select curve to divide")
    if not curve_info: return 1
    curve = curve_info[0]
    
    default_length = None
    if sc.sticky.has_key("knCenterDivide_LastLength"):
        default_length = sc.sticky["knCenterDivide_LastLength"]
    
    seg_length = rs.GetReal("Segment length", default_length, 0.0)
    if not seg_length: return 1
    
    sc.sticky["knCenterDivide_LastLength"] = seg_length
    
    total_length = rs.CurveLength(curve)
    
    if total_length <= seg_length:
        print("Curve is shorter than the segment length.")
        return 1
        
    num_segments = int(total_length // seg_length)
    total_seg_length = num_segments * seg_length
    remainder = total_length - total_seg_length
    
    start_offset = remainder / 2.0
    
    points_to_add = []
    
    for i in range(num_segments + 1):
        dist = start_offset + (i * seg_length)
        if dist > total_length: dist = total_length 
        
        pt = rs.CurveArcLengthPoint(curve, dist)
        if pt:
            points_to_add.append(pt)
            
    if points_to_add:
        rs.AddPoints(points_to_add)
        print("Divided with equal leftovers. Start/End offset is {:.2f} mm").format(start_offset)
        
    return 0

if __name__ == "__main__":
    RunCommand(True)
