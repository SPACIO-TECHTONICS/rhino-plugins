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
from System.Drawing import Color  # type: ignore



colorsDict = {"URBAN3D::Type::residential":"255,0,0",
              "URBAN3D::Type::commercial":"0,255,0",
              "URBAN3D::Type::parking":"0,0,255"}

def StoreasDocumentUserText(dict):
    keys = dict.keys()
    values = dict.values()
    for i in range(len(keys)):
        rs.SetDocumentUserText(str(keys[i]),str(values[i]))

def TransferObjUserText(fromId,toId):
    keys = rs.GetUserText(fromId)
    #values = []
    for key in keys:
        value = rs.GetUserText(fromId,key)
        rs.SetUserText(toId,key,value)

def CreatePlanarSrfsfromCurves(ids):
    srfcrvs = []
    srfs = []
    for each in ids:
        srfcrvs.append(rs.coercecurve(each))
    breps = rg.Brep.CreatePlanarBreps(srfcrvs)
    for brep in breps :
        srfs.append(sc.doc.Objects.AddBrep(brep))
    
    return srfs

def StringswithSubstring(substring, string_array):
    matching_strings = []
    for string in string_array:
        if substring in string:
            matching_strings.append(string)
    return matching_strings

def ClearDocumentTextswithSubstring(substring):
    keys_to_be_deleted = StringswithSubstring(substring,rs.GetDocumentUserText())
    #print keys_to_be_deleted
    for key in keys_to_be_deleted:
        rs.SetDocumentUserText(key)


def tuple_to_color(rgb_tuple):
    r, g, b = rgb_tuple
    color = Color.FromArgb(r, g, b)
    return color

def get_height_from_tags(attributes, default_level_height=3.5):
    """
    Parses OSM attributes to find height or building levels.
    """
    import re
    
    # 1. Direct height tag
    if 'height' in attributes:
        h_str = attributes['height']
        match = re.search(r"([0-9.]+)", h_str)
        if match:
            return float(match.group(1))
            
    # 2. Building levels tag
    if 'building:levels' in attributes:
        levels_str = attributes['building:levels']
        match = re.search(r"([0-9.]+)", levels_str)
        if match:
            return float(match.group(1)) * default_level_height
            
    # 3. Default (if it is a building)
    if 'building' in attributes:
        return default_level_height
        
    return 0.0

def get_min_height_from_tags(attributes, default_level_height=3.5):
    """
    Parses OSM attributes to find min_height or min_level.
    """
    import re
    if 'min_height' in attributes:
        h_str = attributes['min_height']
        match = re.search(r"([0-9.]+)", h_str)
        if match:
            return float(match.group(1))
            
    if 'building:min_level' in attributes:
        levels_str = attributes['building:min_level']
        match = re.search(r"([0-9.]+)", levels_str)
        if match:
            return float(match.group(1)) * default_level_height
            
    return 0.0


