# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino.Commands


def get_collective_bounding_box(object_ids):
    """
    Calculates the union bounding box for a list of Rhino objects.
    """
    if not object_ids:
        return None

    bbox = rg.BoundingBox.Empty
    for obj_id in object_ids:
        obj = rs.coercerhinoobject(obj_id)
        if obj:
            bbox.Union(obj.Geometry.GetBoundingBox(True))

    return bbox


def create_layer_if_missing(layer_name, layer_color=None):
    """
    Creates a layer if it doesn't exist. Optionally sets color.
    """
    if not rs.IsLayer(layer_name):
        rs.AddLayer(layer_name, layer_color)
    return layer_name


def safe_run_command(func):
    """
    Decorator for Rhino commands to ensure authentication and basic error handling.
    """

    def wrapper(is_interactive):
        try:
            try:
                from assets import auth_helper

                if not auth_helper.ensure_authenticated("UrbanDesign4Rhino"):
                    return Rhino.Commands.Result.Cancel
            except Exception as e:
                print("Auth check bypassed: {0}".format(e))

            return func(is_interactive)

        except Exception as e:
            import traceback

            print("Command Error: {0}".format(e))
            print(traceback.format_exc())
            return Rhino.Commands.Result.Failure

    return wrapper
