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

layer_conditions = [
  {'layer_name':'URBAN2D::buildings',  
   'conditions': [ ['building','*'] ]},
   
   
   
  # cycleways
  {'layer_name':'URBAN2D::road::cycle_bridge',  
   'conditions': [ ['highway','cycleway'],  
                   ['bridge','*'] ]},
                   
  {'layer_name':'URBAN2D::road::cycle_embankment',  
   'conditions': [ ['highway','cycleway'],  
                   ['embankment','*'] ]},

  {'layer_name':'URBAN2D::road::cycle',  
   'conditions': [ ['highway','cycleway'] ]},

  # redestrian roads and paths
  {'layer_name':'URBAN2D::pedestrian::steps',  
   'conditions': [ ['highway','steps'] ]},
  {'layer_name':'URBAN2D::pedestrian::footway_bridge',  
   'conditions': [ ['highway','footway'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::footway_tunnel',  
   'conditions': [ ['highway','footway'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::footway_embankment',  
   'conditions': [ ['highway','footway'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::footway',  
   'conditions': [ ['highway','footway'] ]},
  {'layer_name':'URBAN2D::pedestrian::path_bridge',  
   'conditions': [ ['highway','path'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::pedestrian_path_tunnel',  
   'conditions': [ ['highway','path'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::path_embankment',  
   'conditions': [ ['highway','path'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::path', 
   'conditions': [ ['highway','path'] ]},
  
  # pedestrian streets
  {'layer_name':'URBAN2D::pedestrian::area',  
   'conditions': [ ['highway','pedestrian'],
                   ['area', '*'] ]},
  {'layer_name':'URBAN2D::pedestrian::bridge',  
   'conditions': [ ['highway','pedestrian'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::tunnel',  
   'conditions': [ ['highway','pedestrian'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::embankment',  
   'conditions': [ ['highway','pedestrian'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::pedestrian::area',  
   'conditions': [ ['highway','pedestrian'] ]},
   
  # roads
  {'layer_name':'URBAN2D::road::motorway_bridge',  
   'conditions': [ ['highway','motorway'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::motorway_tunnel',  
   'conditions': [ ['highway','motorway'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road::motorway_embankment',  
   'conditions': [ ['highway','motorway'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road_motorway',  
   'conditions': [ ['highway','motorway'] ]},
  {'layer_name':'URBAN2D::road::motorway_link',  
   'conditions': [ ['highway','motorway_link'] ]},
   
  {'layer_name':'URBAN2D::road::trunk_bridge',  
   'conditions': [ ['highway','trunk'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::trunk_tunnel',  
   'conditions': [ ['highway','trunk'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road_trunk_embankment',  
   'conditions': [ ['highway','trunk'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road::trunk',  
   'conditions': [ ['highway','trunk'] ]},
  {'layer_name':'URBAN2D::road::trunk_link',  
   'conditions': [ ['highway','trunk_link'] ]},
   
  {'layer_name':'URBAN2D::road::primary_bridge',  
   'conditions': [ ['highway','primary'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::primary_tunnel',  
   'conditions': [ ['highway','primary'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road::primary_embankment',  
   'conditions': [ ['highway','primary'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road::primary',  
   'conditions': [ ['highway','primary'] ]},
  {'layer_name':'URBAN2D::road::primary_link',  
   'conditions': [ ['highway','primary_link'] ]},
   
  {'layer_name':'URBAN2D::road_secondary_bridge',  
   'conditions': [ ['highway','secondary'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::secondary_tunnel',  
   'conditions': [ ['highway','secondary'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road::secondary_embankment',  
   'conditions': [ ['highway','secondary'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road::secondary',  
   'conditions': [ ['highway','secondary'] ]},
  {'layer_name':'URBAN2D::road_secondary_link',  
   'conditions': [ ['highway','secondary_link'] ]},
   
  {'layer_name':'URBAN2D::road::secondary_bridge',  
   'conditions': [ ['highway','secondary'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::secondary_tunnel',  
   'conditions': [ ['highway','secondary'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road::tertiary_embankment',  
   'conditions': [ ['highway','tertiary'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road::tertiary',  
   'conditions': [ ['highway','tertiary'] ]},
  {'layer_name':'URBAN2D::road::tertiary_link',  
   'conditions': [ ['highway','tertiary_link'] ]},

  {'layer_name':'URBAN2D::road::track_bridge',  
   'conditions': [ ['highway','track'],
                   ['bridge','*']  ]},
  {'layer_name':'URBAN2D::road::track_tunnel',  
   'conditions': [ ['highway','track'],
                   ['tunnel','*']  ]},
  {'layer_name':'URBAN2D::road::track_embankment',  
   'conditions': [ ['highway','track'],
                   ['embankment','*']  ]},
  {'layer_name':'URBAN2D::road::track',  
   'conditions': [ ['highway','track'] ]},
   
  {'layer_name':'URBAN2D::road::residential',  
   'conditions': [ ['highway','living_street'] ]},
  {'layer_name':'URBAN2D::road::residential',  
   'conditions': [ ['highway','residential'] ]},
   
  {'layer_name':'URBAN2D::road_service',  
   'conditions': [ ['highway','service'] ]},

  {'layer_name':'URBAN2D::road::unknown',  
   'conditions': [ ['highway','road'] ]},
   
  {'layer_name':'URBAN2D::road::proposed',  
   'conditions': [ ['highway','proposed'] ]},
  {'layer_name':'URBAN2D::road::proposed',  
   'conditions': [ ['highway','construction'] ]},
   
  {'layer_name':'URBAN2D::road::other',  
   'conditions': [ ['highway','*'] ]},
    
  # railways
  {'layer_name':'URBAN2D::railway::tram_bridge',  
   'conditions': [ ['railway','tram'],
                   ['bridge','*'] ]},
                   
  {'layer_name':'URBAN2D::railway::tram_embankment',  
   'conditions': [ ['railway','tram'],
                   ['embankment','*'] ]},
                   
  {'layer_name':'URBAN2D::railway_tram_tunnel',  
   'conditions': [ ['railway','tram'],
                   ['tunnel','*'] ]},
                   
  {'layer_name':'URBAN2D::railway_tram',  
   'conditions': [ ['railway','tram'] ]},
   
  {'layer_name':'URBAN2D::railway::subway',  
   'conditions': [ ['railway','subway'] ]},
  
  
  {'layer_name':'URBAN2D::railway::bridge',  
   'conditions': [ ['railway','rail'],
                   ['bridge','*'] ]},
  {'layer_name':'URBAN2D::railway::bridge',  
   'conditions': [ ['railway','light_rail'],
                   ['bridge','*'] ]},
                   
  {'layer_name':'URBAN2D::railway::embankment',  
   'conditions': [ ['railway','rail'],
                   ['embankment','*'] ]},
  {'layer_name':'URBAN2D::railway::embankment',  
   'conditions': [ ['railway','light_rail'],
                   ['embankment','*'] ]},

  {'layer_name':'URBAN2D::railway::tunnel',  
   'conditions': [ ['railway','rail'],
                   ['tunnel','*'] ]},
  {'layer_name':'URBAN2D::railway::tunnel',  
   'conditions': [ ['railway','light_rail'],
                   ['tunnel','*'] ]},
                   
  {'layer_name':'URBAN2D::railway::rail',  
   'conditions': [ ['railway','rail'] ]},
  {'layer_name':'URBAN2D::railway::rail',  
   'conditions': [ ['railway','light_rail'] ]},
  {'layer_name':'URBAN2D::railway::other',  
   'conditions': [ ['railway','*'] ]},
  
  # aerialways
  {"layer_name": "URBAN2D::aerial::tram", 
   "conditions": [ ["aerialway","cable_car"] ]},
  {"layer_name": "URBAN2D::aerial::tram chair", 
   "conditions": [ ["aerialway","chair_lift"] ]},
  {"layer_name": "URBAN2D::aerial::tram chair", 
   "conditions": [ ["aerialway","gondola"] ]},
  {"layer_name": "URBAN2D::aerial::tram chair", 
   "conditions": [ ["aerialway","mixed_lift"] ]},

  {"layer_name": "URBAN2D::aeroway", 
   "conditions": [ ["aeroway","aerodrome"] ]},
  {"layer_name": "URBAN2D::aeroway", 
   "conditions": [ ["aeroway","apron"] ]},
  {"layer_name": "URBAN2D::aeroway", 
   "conditions": [ ["aeroway","helipad"] ]},
  {"layer_name": "URBAN2D::aeroway", 
   "conditions": [ ["aeroway","runway"] ]},
  {"layer_name": "URBAN2D::aeroway", 
   "conditions": [ ["aeroway","taxiway"] ]},
  
  # water
  {"layer_name": "URBAN2D::water", 
   "conditions": [ ["natural","water"] ]},
  {"layer_name": "URBAN2D::water", 
   "conditions": [ ["natural","spring"] ]},
  {"layer_name": "URBAN2D::water", 
   "conditions": [ ["natural","riverbank"] ]},
  {"layer_name": "URBAN2D::water", 
   "conditions": [ ["leisure","marina"] ]},
  {"layer_name": "URBAN2D::coast", 
   "conditions": [ ["natural","coast"] ]},
  
  # green
  {"layer_name": "URBAN2D::park", 
   "conditions": [ ["leisure","park"] ]},
  {"layer_name": "URBAN2D::park", 
   "conditions": [ ["leisure","garden"] ]},
  {"layer_name": "URBAN2D::park", 
   "conditions": [ ["leisure","village_green"] ]},
  {"layer_name": "URBAN2D::forest", 
   "conditions": [ ["landuse","forest"] ]},
  {"layer_name": "URBAN2D::forest", 
   "conditions": [ ["natural","wood"] ]},
   
  # playgrounds
  {"layer_name": "URBAN2D::sport", 
   "conditions": [ ["leisure","pitch"] ]},
  {"layer_name": "URBAN2D::sport", 
   "conditions": [ ["leisure","stadium"] ]},
  
  # boundary
  {"layer_name": "URBAN2D::borders", 
   "conditions": [ ["boundary","administrative"] ]},
  
  # contours
  {"layer_name": "URBAN2D::contours::major", 
   "conditions": [ ["contour_ext","elevation_major"] ]},
  {"layer_name": "URBAN2D::contours::minor", 
   "conditions": [ ["contour","elevation"] ]},
  
  # rest
  {'layer_name':'URBAN2D::other',  
   'conditions': [ ['*','*'] ]}
]
