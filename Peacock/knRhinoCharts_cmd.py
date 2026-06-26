# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import Rhino
import scriptcontext as sc
import os

import sys

plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

from assets import charts_panel
if sys.version_info.major >= 3:
    import importlib
    importlib.reload(charts_panel)
else:
    reload(charts_panel)

from charts_panel import PeacockDashboard

if '__dashboard_instance' not in globals():
    __dashboard_instance = None

def RunCommand(is_interactive):


global __dashboard_instance
    
    if __dashboard_instance:
        try:
            if __dashboard_instance.Visible:
                __dashboard_instance.BringToFront()
                __dashboard_instance.Focus()
                return Rhino.Commands.Result.Success
            else:
                __dashboard_instance = None
        except:
            __dashboard_instance = None
            
    try:
        __dashboard_instance = PeacockDashboard()
        
        __dashboard_instance.Show()
        
        return Rhino.Commands.Result.Success
    except Exception as ex:
        Rhino.RhinoApp.WriteLine("Peacock Error: {}".format(ex))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
