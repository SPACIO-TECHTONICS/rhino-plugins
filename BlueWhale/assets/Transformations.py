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
from scriptcontext import doc
from System import Array  # type: ignore
import Rhino.Geometry as rg  # type: ignore


def string_to_matrix(transform_str):
    # Split the string by comma and extract the values
    values = transform_str.replace('=', ',').replace('(', '').replace(')', '').split(',')
    
    elements = [float(value) for value in values if 'R' not in value.strip()]

    transformation = rg.Transform()

    # Create a 4x4 transformation matrix
    matrix_array = [
        [elements[0], elements[1], elements[2], elements[3]],
        [elements[4], elements[5], elements[6], elements[7]],
        [elements[8], elements[9], elements[10], elements[11]],
        [elements[12], elements[13], elements[14], elements[15]]
    ]
    
    # Populate the transformation matrix with the values from the array
    for i in range(4):
        for j in range(4):
            transformation[i, j] = matrix_array[i][j]

    return transformation





"""
if __name__ == "__main__":
    # Given transformation string
    transform_str = "R0=(1,0,0,8867135.38268291), R1=(0,1,0,1347933.35031309), R2=(0,0,1,0), R3=(0,0,0,1)"

    # Convert string to transformation matrix
    matrix = string_to_matrix(transform_str)

    print("Transformation Matrix:")
    print(matrix)"""
