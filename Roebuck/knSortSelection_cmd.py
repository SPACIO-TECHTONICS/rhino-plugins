"""Sorts selected objects by their bounding box centers along X, Y, or Z axes, and stores the sorted list in memory for knDistributeonCurve."""

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knSortSelection" # RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"

def RunCommand( is_interactive ):
    print "Hello", __commandname__
    
    # 1. Get objects (can be selected all at once via window select)
    objects = rs.GetObjects("Select objects to sort", preselect=True)
    if not objects: return 1
    
    # 2. Check memory for previous sorting preference
    default_sort = "X_LeftToRight"
    if sc.sticky.has_key("knSortSelection_LastSort"):
        default_sort = sc.sticky["knSortSelection_LastSort"]
        
    options = [
        "X_LeftToRight", "X_RightToLeft", 
        "Y_BottomToTop", "Y_TopToBottom", 
        "Z_LowToHigh", "Z_HighToLow"
    ]
    
    # 3. Ask user for sort direction
    sort_method = rs.GetString("Sort direction based on object centers", default_sort, options)
    if not sort_method: return 1
    
    sc.sticky["knSortSelection_LastSort"] = sort_method
    
    sortable_list = []
    
    # 4. Calculate centers and assign sorting values
    for obj in objects:
        bbox = rs.BoundingBox(obj)
        if not bbox: continue
        
        # Calculate true 3D center of the bounding box
        cx = (bbox[0].X + bbox[2].X) / 2.0
        cy = (bbox[0].Y + bbox[2].Y) / 2.0
        cz = (bbox[0].Z + bbox[4].Z) / 2.0
        
        # Assign the value to sort by based on user selection
        if sort_method == "X_LeftToRight": val = cx
        elif sort_method == "X_RightToLeft": val = -cx
        elif sort_method == "Y_BottomToTop": val = cy  # Plan view: Bottom to Top
        elif sort_method == "Y_TopToBottom": val = -cy # Plan view: Top to Bottom
        elif sort_method == "Z_LowToHigh": val = cz    # Elevation: Bottom to Top
        elif sort_method == "Z_HighToLow": val = -cz   # Elevation: Top to Bottom
        else: val = cx # Fallback
        
        # Store a tuple of (value, object_id)
        sortable_list.append((val, obj))
        
    # 5. Sort the list numerically based on the coordinate values
    sortable_list.sort(key=lambda x: x[0])
    
    # 6. Extract the newly sorted object IDs
    sorted_objects = [item[1] for item in sortable_list]
    
    # 7. SYNERGY: Save this directly to the Distribute tool's memory!
    sc.sticky["knDistributeonCurve_LastObjects"] = sorted_objects
    
    # Highlight the objects so the user knows it finished
    rs.UnselectAllObjects()
    rs.SelectObjects(sorted_objects)
    
    print "Successfully sorted {} objects by {}. Ready for knDistributeonCurve!".format(len(sorted_objects), sort_method)
    
    # you can optionally return a value from this function
    # to signify command result. Return values that make
    # sense are
    # 0 == success
    # 1 == cancel
    # If this function does not return a value, success is assumed
    return 0

RunCommand(True)