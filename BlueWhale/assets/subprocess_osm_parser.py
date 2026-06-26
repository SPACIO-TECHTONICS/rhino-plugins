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

import os
import subprocess
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

# Set the input and output files
osm_file = "C:/path/to/osm/file.osm"
dxf_file = "C:/path/to/dxf/file.dxf"

# Convert the OSM data to DXF format using ogr2ogr
subprocess.check_call(["ogr2ogr", "-f", "DXF", dxf_file, osm_file])

# Import the DXF file into Rhino
sc.doc.Import(dxf_file)