# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import Rhino.Geometry as rg


def string_to_matrix(transform_str):
    values = (
        transform_str.replace("=", ",").replace("(", "").replace(")", "").split(",")
    )

    elements = [float(value) for value in values if "R" not in value.strip()]

    transformation = rg.Transform()

    matrix_array = [
        [elements[0], elements[1], elements[2], elements[3]],
        [elements[4], elements[5], elements[6], elements[7]],
        [elements[8], elements[9], elements[10], elements[11]],
        [elements[12], elements[13], elements[14], elements[15]],
    ]

    for i in range(4):
        for j in range(4):
            transformation[i, j] = matrix_array[i][j]

    return transformation


"""
if __name__ == "__main__":
    transform_str = "R0=(1,0,0,8867135.38268291), R1=(0,1,0,1347933.35031309), R2=(0,0,1,0), R3=(0,0,0,1)"

    matrix = string_to_matrix(transform_str)

    print("Transformation Matrix:")
    print(matrix)"""
