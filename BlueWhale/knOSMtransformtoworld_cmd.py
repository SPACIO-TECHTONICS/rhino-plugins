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
import Rhino  # type: ignore
import Rhino.Geometry as rg  # type: ignore
from assets import auth_helper
from assets.Transformations import string_to_matrix

__commandname__ = "knOSMtransformtoworld"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knOSMtransformtoworld"):
        return auth_helper.get_cancel_result()

    matrix_str = rs.GetDocumentUserText("Transformation Matrix")
    if not matrix_str:
        rs.MessageBox("No transformation matrix found in document. Cannot restore world coordinates.")
        return Rhino.Commands.Result.Failure

    objs = rs.AllObjects()
    if not objs:
        return Rhino.Commands.Result.Cancel

    try:
        matrix = string_to_matrix(matrix_str)
        success, inverted_matrix = matrix.TryGetInverse()
        
        if success:
            rs.EnableRedraw(False)
            rs.TransformObjects(objs, inverted_matrix, False)
            
            # Since we are back at World coordinates (WGS84 projection base), 
            # we should update the tracking text.
            rs.SetDocumentUserText("Model Location", "Global")
            # Clear the transformation matrix as it's no longer 'active' (or keep it but set to identity?)
            # Usually 'Global' means the 0,0,0 is the projection origin.
            
            rs.EnableRedraw(True)
            print("Model restored to World coordinates.")
            return Rhino.Commands.Result.Success
        else:
            rs.MessageBox("Failed to invert the transformation matrix.")
            return Rhino.Commands.Result.Failure

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error transforming to world: {0}".format(e))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
