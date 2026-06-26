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