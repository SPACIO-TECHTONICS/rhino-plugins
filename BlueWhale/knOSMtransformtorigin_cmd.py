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

import rhinoscriptsyntax as rs  # type: ignore
import Rhino.Geometry as rg  # type: ignore
import scriptcontext as sc  # type: ignore
import math

from assets import osm_logic
from assets import geometry_utilities
from assets import auth_helper
from assets.Transformations import string_to_matrix
from assets.DrawRectangleDisplayNormal import DrawRectangleDisplayNormal

__commandname__ = "knOSMtransformtorigin"

def RunCommand(is_interactive):
    # Authentication & Logging
    if not auth_helper.ensure_authenticated("BlueWhale", "knOSMtransformtorigin"):
        return auth_helper.get_cancel_result()

    # Get existing transformation data
    existing_matrix_str = rs.GetDocumentUserText("Transformation Matrix")
    existing_origin_str = rs.GetDocumentUserText("GeoLocated Origin")

    tol = sc.doc.ModelAbsoluteTolerance 
    sc.doc.ModelAbsoluteTolerance = 0.01
    
    try:
        # Ask user to pick a new origin/plane
        # This function typically handles the UI for picking a point and returning a plane
        plane = DrawRectangleDisplayNormal()
        if not plane:
            print("Transformation canceled.")
            return Rhino.Commands.Result.Cancel

        # Objects to transform
        objs = rs.AllObjects()
        if not objs:
            rs.MessageBox("No objects found in document to transform.")
            return Rhino.Commands.Result.Cancel

        # 1. Calculate the NEW transformation for this step
        # Transforming from the current plane to WorldXY (i.e. moving current plane origin to 0,0,0)
        new_matrix = rs.XformChangeBasis(rg.Plane.WorldXY, plane)
        
        # 2. Compound with existing transformation
        # The existing matrix tracks [WGS84 -> Current State]
        # The new matrix tracks [Current State -> New State]
        # Combined = New * Existing
        combined_matrix = osm_logic.get_compound_matrix(existing_matrix_str, new_matrix)
        
        # 3. Apply the transformation to the geometry
        rs.TransformObjects(objs, new_matrix, False)
        
        # 4. Update Document User Text
        rs.SetDocumentUserText("Transformation Matrix", str(combined_matrix))
        
        # 5. Update GeoLocated Origin
        # We need the Lat/Long of the point that is now at (0,0,0).
        # We can find this by taking the (0,0,0) point in the current space, 
        # finding its original coordinate, and converting back to Lat/Long.
        # Actually, the 'combined_matrix' already tells us how to get from WGS/Meters to current 0,0,0.
        # To go from current 0,0,0 to WGS/Meters, we use the Inverse of the combined matrix.
        
        inverse_combined = rg.Transform.Empty
        success, inverse_combined = combined_matrix.TryGetInverse()
        if success:
            original_pt = rg.Point3d(0,0,0)
            original_pt.Transform(inverse_combined)
            
            new_lat = osm_logic.meters_to_lat(original_pt.Y)
            new_lon = osm_logic.meters_to_lon(original_pt.X)
            
            rs.SetDocumentUserText("GeoLocated Origin", "{0}, {1}".format(new_lat, new_lon))
            rs.SetDocumentUserText("Model Location", "Local")
            
            print("Transformation compounded. New Geo-Origin: {0}, {1}".format(new_lat, new_lon))
        else:
            print("Warning: Could not calculate inverse matrix for geo-tracking.")

        return Rhino.Commands.Result.Success

    except Exception as e:
        import traceback
        print("Transformation Error: {0}".format(e))
        print(traceback.format_exc())
        return Rhino.Commands.Result.Failure
    finally:
        sc.doc.ModelAbsoluteTolerance = tol

if __name__ == "__main__":
    RunCommand(True)
