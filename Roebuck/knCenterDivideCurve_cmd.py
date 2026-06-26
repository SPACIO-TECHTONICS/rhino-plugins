import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knCenterDivideCurve" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):


print("Executing " + __commandname__)
    
    # Get the curve
    curve_info = rs.GetCurveObject("Select curve to divide")
    if not curve_info: return 1
    curve = curve_info[0]
    
    # 1. Check memory for previous length; default to None (blank) on first run
    default_length = None
    if sc.sticky.has_key("knCenterDivide_LastLength"):
        default_length = sc.sticky["knCenterDivide_LastLength"]
    
    # 2. Ask user for segment length
    seg_length = rs.GetReal("Segment length", default_length, 0.0)
    if not seg_length: return 1
    
    # 3. Save the new value back to memory for next time
    sc.sticky["knCenterDivide_LastLength"] = seg_length
    
    total_length = rs.CurveLength(curve)
    
    if total_length <= seg_length:
        print("Curve is shorter than the segment length.")
        return 1
        
    # Calculate number of full segments and remainder
    num_segments = int(total_length // seg_length)
    total_seg_length = num_segments * seg_length
    remainder = total_length - total_seg_length
    
    # Divide the leftover equally for both sides
    start_offset = remainder / 2.0
    
    # Create points list
    points_to_add = []
    
    # Calculate and plot the division points
    for i in range(num_segments + 1):
        dist = start_offset + (i * seg_length)
        # Prevent floating point errors from exceeding curve length
        if dist > total_length: dist = total_length 
        
        pt = rs.CurveArcLengthPoint(curve, dist)
        if pt:
            points_to_add.append(pt)
            
    # Add points to the document
    if points_to_add:
        rs.AddPoints(points_to_add)
        print("Divided with equal leftovers. Start/End offset is {:.2f} mm").format(start_offset)
        
    return 0

if __name__ == "__main__":
    RunCommand(True)
