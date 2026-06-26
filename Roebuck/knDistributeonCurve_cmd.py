"""Distributes selected objects along a path curve at specific segment intervals, aligning them via a specified base point (bottom/top center) with optional 3D/XY/Z movement constraints."""

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knDistributeonCurve" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # 1. Object Selection Memory Logic
    objects = None
    valid_saved = []
    
    # Check memory for previously saved objects
    if sc.sticky.has_key("knDistributeonCurve_LastObjects"):
        saved_guids = sc.sticky["knDistributeonCurve_LastObjects"]
        valid_saved = [g for g in saved_guids if rs.IsObject(g)]
        
    if valid_saved and not rs.SelectedObjects():
        use_prev = rs.GetString("Use the {} previously selected objects in their original order?".format(len(valid_saved)), "Yes", ["Yes", "No"])
        if use_prev and use_prev.lower() == "yes":
            objects = valid_saved
            rs.SelectObjects(objects)
            
    if not objects:
        objects = rs.GetObjects("Select distinct objects to distribute (select sequentially for order)", preselect=True)
        
    if not objects: return 1
    
    sc.sticky["knDistributeonCurve_LastObjects"] = objects
    
    # 2. Get the path curve
    curve_info = rs.GetCurveObject("Select path curve")
    if not curve_info: return 1
    curve = curve_info[0]
    
    # 3. Check memory for previous settings
    default_length = None
    if sc.sticky.has_key("knDistributeonCurve_LastLength"):
        default_length = sc.sticky["knDistributeonCurve_LastLength"]
        
    default_align = "BottomCenter"
    if sc.sticky.has_key("knDistributeonCurve_LastAlign"):
        default_align = sc.sticky["knDistributeonCurve_LastAlign"]
        
    default_keep = "Yes"
    if sc.sticky.has_key("knDistributeonCurve_LastKeep"):
        default_keep = sc.sticky["knDistributeonCurve_LastKeep"]
        
    default_constraint = "3D"
    if sc.sticky.has_key("knDistributeonCurve_LastConstraint"):
        default_constraint = sc.sticky["knDistributeonCurve_LastConstraint"]
    
    # 4. Ask user for parameters
    seg_length = rs.GetReal("Segment length (distance between items)", default_length, 0.0)
    if not seg_length: return 1
    
    alignment = rs.GetString("Base point alignment", default_align, ["BottomCenter", "TopCenter"])
    if not alignment: return 1
    
    constraint = rs.GetString("Movement constraint", default_constraint, ["3D", "XY_Only", "Z_Only"])
    if not constraint: return 1
    
    keep_original = rs.GetString("Keep original objects?", default_keep, ["Yes", "No"])
    if not keep_original: return 1
    
    # Save the new values back to memory
    sc.sticky["knDistributeonCurve_LastLength"] = seg_length
    sc.sticky["knDistributeonCurve_LastAlign"] = alignment
    sc.sticky["knDistributeonCurve_LastKeep"] = keep_original
    sc.sticky["knDistributeonCurve_LastConstraint"] = constraint
    
    # Calculate spacing logic
    total_length = rs.CurveLength(curve)
    
    if total_length <= seg_length:
        print "Curve is shorter than the segment length."
        return 1
        
    num_segments = int(total_length // seg_length)
    total_seg_length = num_segments * seg_length
    remainder = total_length - total_seg_length
    
    start_offset = remainder / 2.0
    
    # Calculate division points
    points_to_add = []
    for i in range(num_segments + 1):
        dist = start_offset + (i * seg_length)
        if dist > total_length: dist = total_length 
        
        pt = rs.CurveArcLengthPoint(curve, dist)
        if pt:
            points_to_add.append(pt)
            
    if not points_to_add:
        return 1

    rs.EnableRedraw(False)
    placed_count = 0
    
    # Distribute objects
    for i in range(min(len(objects), len(points_to_add))):
        obj = objects[i]
        target_pt = points_to_add[i]
        
        bbox = rs.BoundingBox(obj)
        if not bbox: continue
        
        # Calculate Base Point
        center_x = (bbox[0].X + bbox[2].X) / 2.0
        center_y = (bbox[0].Y + bbox[2].Y) / 2.0
        
        if alignment.lower() == "topcenter":
            base_pt = [center_x, center_y, bbox[4].Z]
        else:
            base_pt = [center_x, center_y, bbox[0].Z]
            
        t = rs.CurveClosestPoint(curve, target_pt)
        tangent = rs.CurveTangent(curve, t)
        
        # Base orientation
        ref_0 = base_pt
        ref_1 = rs.PointAdd(base_pt, [1, 0, 0])
        
        # Apply Constraints
        tgt_x = target_pt.X
        tgt_y = target_pt.Y
        tgt_z = target_pt.Z
        
        tgt_tan_x = tangent.X
        tgt_tan_y = tangent.Y
        tgt_tan_z = tangent.Z
        
        if constraint.lower() == "xy_only":
            tgt_z = base_pt[2] # Keep original Z elevation
            tgt_tan_z = 0      # Flatten rotation to XY plane
            if tgt_tan_x == 0 and tgt_tan_y == 0: tgt_tan_x = 1
                
        elif constraint.lower() == "z_only":
            tgt_x = base_pt[0] # Keep original X position
            tgt_y = base_pt[1] # Keep original Y position
            # Do not rotate the object if it's not following the path in plan
            tgt_tan_x = 1
            tgt_tan_y = 0
            tgt_tan_z = 0
            
        tgt_0 = [tgt_x, tgt_y, tgt_z]
        tgt_1 = rs.PointAdd(tgt_0, [tgt_tan_x, tgt_tan_y, tgt_tan_z])
        
        # Copy and orient
        new_obj = rs.CopyObject(obj)
        rs.OrientObject(new_obj, [ref_0, ref_1], [tgt_0, tgt_1])
        placed_count += 1
        
    # Clean up originals if requested
    if keep_original.lower() == "no":
        rs.DeleteObjects(objects)
        sc.sticky.pop("knDistributeonCurve_LastObjects", None)
        
    rs.EnableRedraw(True)
    
    print "Distributed {} objects. Start/End offset is {:.2f}".format(placed_count, start_offset)
    return 0

RunCommand(True)