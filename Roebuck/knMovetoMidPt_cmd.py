"""Moves selected objects from a base point to the exact midpoint between two clicked target points or to a point along a curve."""

import rhinoscriptsyntax as rs  # type: ignore
import Rhino.Geometry as rg  # type: ignore
import Rhino  # type: ignore

__commandname__ = "knMovetoMidPt"

def RunCommand(is_interactive):


# Select objects to move
    objIds = rs.GetObjects("Select objects to move", preselect=True)
    if not objIds: return 1
    
    # Select base point
    base_pt = rs.GetPoint("Select base point (point to move from)")
    if not base_pt: return 1
    
    # Options for target midpoint
    pt1 = rs.GetPoint("Select first target point (or press Enter to select a curve)")
    
    if pt1:
        pt2 = rs.GetPoint("Select second target point", base_point=pt1)
        if not pt2: return 1
        mid_pt = (pt1 + pt2) / 2.0
    else:
        # Select target line or curve for its midpoint
        target = rs.GetObject("Select target line or curve for midpoint alignment", 
                              rs.filter.curve | rs.filter.edgeobject)
        if not target: return 1
        
        # Calculate midpoint using normalized parameter 0.5
        curve = rs.coercecurve(target)
        if not curve:
            print("Invalid target: not a curve or edge.")
            return 1
        mid_pt = curve.PointAtNormalizedParameter(0.5)
    
    # Execute move
    translation = mid_pt - base_pt
    rs.MoveObjects(objIds, translation)
    
    print("Moved {} objects to midpoint.".format(len(objIds)))
    
    return 0

if __name__ == "__main__":
    RunCommand(True)
