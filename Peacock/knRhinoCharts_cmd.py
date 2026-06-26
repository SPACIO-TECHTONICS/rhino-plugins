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

from __future__ import print_function
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore
import os

import sys

# Ensure the current directory is in sys.path
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

from assets import charts_panel
# Force reload the module to handle changes made during development
# This is crucial in Rhino where modules stay in sys.modules across script runs
if sys.version_info.major >= 3:
    import importlib
    importlib.reload(charts_panel)
else:
    reload(charts_panel)

from charts_panel import PeacockDashboard

# Global variable to track the open dashboard instance across command calls
# This ensures we only have one singleton instance
if '__dashboard_instance' not in globals():
    __dashboard_instance = None

def RunCommand(is_interactive):


global __dashboard_instance
    
    # Handle Singleton Instance
    if __dashboard_instance:
        try:
            # If it's already open, just bring it to front
            if __dashboard_instance.Visible:
                __dashboard_instance.BringToFront()
                __dashboard_instance.Focus()
                return Rhino.Commands.Result.Success
            else:
                # If it was closed/hidden, prepare to recreate
                __dashboard_instance = None
        except:
            # Handle disposed objects
            __dashboard_instance = None
            
    # Create and show new dashboard
    try:
        __dashboard_instance = PeacockDashboard()
        
        # We use .Show() for modeless behavior (doesn't block Rhino)
        __dashboard_instance.Show()
        
        return Rhino.Commands.Result.Success
    except Exception as ex:
        Rhino.RhinoApp.WriteLine("Peacock Error: {}".format(ex))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
