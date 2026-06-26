# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import math
import Rhino.Geometry as rg

EARTH_RADIUS = 6378137.0


def lat_to_meters(lat):
    """
    Converts latitude (degrees) to Y coordinate (meters) using Mercator projection.
    """
    lat_rad = math.radians(lat)
    return EARTH_RADIUS * math.log((math.sin(lat_rad) + 1.0) / math.cos(lat_rad))


def lon_to_meters(lon):
    """
    Converts longitude (degrees) to X coordinate (meters).
    """
    return EARTH_RADIUS * math.radians(lon)


def meters_to_lat(y):
    """
    Converts Y coordinate (meters) to latitude (degrees) using inverse Mercator projection.
    """
    return math.degrees(2.0 * math.atan(math.exp(y / EARTH_RADIUS)) - math.pi / 2.0)


def meters_to_lon(x):
    """
    Converts X coordinate (meters) to longitude (degrees).
    """
    return math.degrees(x / EARTH_RADIUS)


def get_compound_matrix(old_matrix_str, new_matrix):
    """
    Compounds a new transformation matrix with an existing one stored as a string.
    Returns the new combined matrix.
    """
    if not old_matrix_str:
        return new_matrix

    try:
        from assets.Transformations import string_to_matrix

        old_matrix = string_to_matrix(old_matrix_str)
        if not old_matrix:
            return new_matrix

        combined = new_matrix * old_matrix
        return combined
    except Exception as e:
        print("Error compounding matrices: {0}".format(e))
        return new_matrix


def calculate_localization_transform(bounding_box):
    """
    Calculates the transformation matrix to move the center of a bounding box to the origin (0,0,0).
    """
    center = bounding_box.Center
    translation = rg.Transform.Translation(-center.X, -center.Y, -center.Z)
    return translation, center
