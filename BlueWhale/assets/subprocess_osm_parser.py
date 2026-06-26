# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import subprocess
import scriptcontext as sc

osm_file = "C:/path/to/osm/file.osm"
dxf_file = "C:/path/to/dxf/file.dxf"

subprocess.check_call(["ogr2ogr", "-f", "DXF", dxf_file, osm_file])

sc.doc.Import(dxf_file)
