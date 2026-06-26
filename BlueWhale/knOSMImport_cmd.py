# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import os
import Rhino
import Rhino.DocObjects
import rhinoscriptsyntax as rs

from assets.osm_parser import osmNetHandler
from assets.default_conditions import layer_conditions
from assets.osm_utilities import get_height_from_tags, get_min_height_from_tags
from assets import ui_progressform

reload(ui_progressform)
from assets import ui_mapsearch
from assets import osm_logic
from assets import geometry_utilities
from assets import auth_helper

__commandname__ = "knOSMImport"


def getLayerName(attributes):
    layer_name = "Default"
    for layer_condition in layer_conditions:
        pass_layer = False
        for condition in layer_condition["conditions"]:
            if condition[0] != "*" and condition[0] not in attributes:
                pass_layer = True
            elif condition[1] != "*" and attributes[condition[0]] != condition[1]:
                pass_layer = True

        if not pass_layer:
            return layer_condition["layer_name"]
    return layer_name


def getWayPoints(children_id, model):
    lon = model.lon
    lat = model.lat
    result = []
    for x in children_id:
        if x in lon and x in lat:
            result.append(
                [osm_logic.lon_to_meters(lon[x]), osm_logic.lat_to_meters(lat[x]), 0]
            )
    return result


def createCurve(waypoints, layer=None, attributes=None, create_3d=False):
    if not waypoints or len(waypoints) < 2:
        return None

    curve = rs.AddPolyline(waypoints)
    if not curve:
        return None

    if layer:
        rs.ObjectLayer(curve, layer)

    if attributes:
        for key, value in attributes.items():
            rs.SetUserText(curve, str(key), str(value))

    if create_3d and attributes and "building" in attributes:
        height = get_height_from_tags(attributes)
        min_height = get_min_height_from_tags(attributes)

        if height > 0:
            ext_height = height - min_height
            if ext_height > 0:
                ext_id = rs.ExtrudeCurve(
                    curve, rs.AddLine([0, 0, 0], [0, 0, ext_height])
                )
                if ext_id:
                    if min_height > 0:
                        rs.MoveObject(ext_id, [0, 0, min_height])
                    rs.CapPlanarHoles(ext_id)
                    rs.ObjectLayer(ext_id, layer)
                    rs.DeleteObject(curve)
                    for key, value in attributes.items():
                        rs.SetUserText(ext_id, str(key), str(value))
                    return ext_id
    return curve


def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knOSMImport"):
        return auth_helper.get_cancel_result()

    source = rs.ListBox(
        ["File", "Direct_Online"], "Select OSM Source", "OSM Data Source"
    )
    if not source:
        return Rhino.Commands.Result.Cancel

    create_3d = rs.GetString("Create 3D Buildings?", "Yes", ["Yes", "No"]) == "Yes"

    input_file_name = None
    if source == "File":
        input_file_name = rs.OpenFileName("Open OSM File", "OSM Files (*.osm)|*.osm||")
    else:
        bbox_str = ui_mapsearch.show_map_selector()
        if not bbox_str:
            return Rhino.Commands.Result.Cancel

        try:
            bbox = tuple(map(float, bbox_str.split(",")))
            if len(bbox) != 4:
                raise ValueError
            input_file_name = ui_progressform.download_osm_with_progress(bbox)
        except Exception as e:
            rs.MessageBox("Error in BBox or Download: {0}".format(e))
            return Rhino.Commands.Result.Failure

    if not input_file_name or not os.path.exists(input_file_name):
        return Rhino.Commands.Result.Cancel

    try:
        osm_model = osmNetHandler(input_file_name)
        model_elements = osm_model.elements

        total_relations = sum(
            len(rel_dict) for rel_dict in model_elements["relation"].values()
        )
        total_ways = len(model_elements["way"])
        total_elements = total_relations + total_ways

        progress_dialog = ui_progressform.ModelCreationProgress(
            total_elements, "Creating 3D Model..."
        )
        progress_dialog.show()
        current_step = 0

        rs.EnableRedraw(False)
        created_ids = []

        for layer_info in layer_conditions:
            ln = layer_info["layer_name"]
            geometry_utilities.create_layer_if_missing(
                ln, layer_info.get("layer_color", (150, 150, 150))
            )

        used_ways = set()
        for rel_type, rel_dict in model_elements["relation"].items():
            for id, relation in rel_dict.items():
                current_step += 1
                if current_step % 5 == 0:
                    progress_dialog.update(
                        current_step,
                        "Processing Relation {0}/{1}...".format(
                            current_step, total_elements
                        ),
                    )

                if rel_type != "multipolygon":
                    continue

                curves = []
                for way_id in relation["children"]:
                    if way_id not in model_elements["way"]:
                        continue
                    used_ways.add(way_id)
                    waypoints = getWayPoints(
                        model_elements["way"][way_id]["children"], osm_model
                    )
                    layer_name = getLayerName(relation["attributes"])
                    curve = createCurve(
                        waypoints, layer_name, relation["attributes"], create_3d
                    )
                    if curve:
                        curves.append(curve)
                        created_ids.append(curve)

                if curves:
                    group_name = relation["attributes"].get(
                        "name", "OSM_Relation_{0}".format(id)
                    )
                    group = rs.AddGroup(group_name)
                    rs.AddObjectsToGroup(curves, group)

        for id, way in model_elements["way"].items():
            current_step += 1
            if current_step % 10 == 0:
                progress_dialog.update(
                    current_step,
                    "Processing Way {0}/{1}...".format(current_step, total_elements),
                )

            if id in used_ways:
                continue
            waypoints = getWayPoints(way["children"], osm_model)
            attributes = way["attributes"]
            obj_id = createCurve(
                waypoints, getLayerName(attributes), attributes, create_3d
            )
            if obj_id:
                created_ids.append(obj_id)

        progress_dialog.update(total_elements, "Geometry Creation Complete.")
        progress_dialog.close()

        if created_ids:
            bbox = geometry_utilities.get_collective_bounding_box(created_ids)
            if bbox:
                xform, center_in_meters = osm_logic.calculate_localization_transform(
                    bbox
                )
                rs.TransformObjects(created_ids, xform, False)
                rs.SetDocumentUserText("Transformation Matrix", str(xform))

                center_lat = osm_logic.meters_to_lat(center_in_meters.Y)
                center_lon = osm_logic.meters_to_lon(center_in_meters.X)
                rs.SetDocumentUserText(
                    "GeoLocated Origin", "{0}, {1}".format(center_lat, center_lon)
                )
                rs.SetDocumentUserText("Model Location", "Local")
                print(
                    "OSM Data localized to origin. Center: {0}, {1} (Lat, Lon)".format(
                        center_lat, center_lon
                    )
                )

        rs.EnableRedraw(True)
        print("OSM Import Successful.")

        layers = sorted(rs.LayerNames(), key=len, reverse=True)
        for layer in layers:
            if rs.IsLayer(layer) and rs.IsLayerEmpty(layer) and layer != "Default":
                rs.DeleteLayer(layer)

        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error during OSM Import: {0}".format(e))
        return Rhino.Commands.Result.Failure


if __name__ == "__main__":
    RunCommand(True)

if __name__ == "__main__":
    RunCommand(True)
