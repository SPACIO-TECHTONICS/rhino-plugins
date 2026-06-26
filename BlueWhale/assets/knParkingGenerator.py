import rhinoscriptsyntax as rs  # type: ignore

def create_parking_stalls(closed_curve, stall_length, stall_width, vehicle_area):
    # Calculate available area inside the closed curve
    available_area = rs.Area(closed_curve)
    
    # Calculate the optimum number of parking stalls
    required_area = stall_length * stall_width + vehicle_area
    num_stalls = int(available_area / required_area)
    
    # Generate parking stall positions
    curve_domain = rs.CurveDomain(closed_curve)
    delta = (curve_domain[1] - curve_domain[0]) / num_stalls
    parking_stalls = []
    
    for i in range(num_stalls):
        t = curve_domain[0] + delta * (i + 0.5)
        point = rs.EvaluateCurve(closed_curve, t)
        parking_stalls.append(point)
    
    # Display the closed curve and parking stalls
    #rs.AddCurve(closed_curve)
    for point in parking_stalls:
        
        rect_plane = rs.PlaneFromNormal(point, rs.VectorCreate[rg.Point3d(0, 0, 1)])
        rect_corners = [
            rs.PointAdd(rect_plane.Origin, rs.VectorScale(rect_plane.XAxis, -stall_length/2)),
            rs.PointAdd(rect_plane.Origin, rs.VectorScale(rect_plane.XAxis, stall_length/2)),
            rs.PointAdd(rect_plane.Origin, rs.VectorScale(rect_plane.YAxis, stall_width/2)),
            rs.PointAdd(rect_plane.Origin, rs.VectorScale(rect_plane.YAxis, -stall_width/2))
        ]
        rs.AddPolyline(rect_corners + [rect_corners[0]])

# Example usage
closed_curve = rs.GetObject("Select a closed curve", rs.filter.curve)
stall_length = 5.0
stall_width = 2.5
vehicle_area = 10.0

create_parking_stalls(closed_curve, stall_length, stall_width, vehicle_area)
