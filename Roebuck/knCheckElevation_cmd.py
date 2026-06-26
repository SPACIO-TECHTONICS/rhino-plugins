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
import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

__commandname__ = "knCheckElevation"

def RunCommand(is_interactive):


# Optional: allow user to define a base elevation (datum)
    base_elevation = 0.0
    
    # Use a GetPoint loop with options
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("Pick point to check elevation")
    
    # Option for base elevation
    optBase = Rhino.Input.Custom.OptionDouble(base_elevation)
    gp.AddOptionDouble("BaseElevation", optBase)
    
    while True:
        res = gp.Get()
        
        if res == Rhino.Input.GetResult.Point:
            pt = gp.Point()
            base_elevation = optBase.CurrentValue
            
            rel_elevation = pt.Z - base_elevation
            
            # Formatting
            unit_system = sc.doc.ModelUnitSystem
            formatted_val = "{:,.3f}".format(rel_elevation)
            result_str = "EL: {} {}".format(formatted_val, str(unit_system).lower())
            print(result_str)
            # Add a permanent text dot for reference
            rs.AddTextDot(result_str, pt)
            
        elif res == Rhino.Input.GetResult.Option:
            continue
        else:
            break
            
    return 0

if __name__ == "__main__":
    RunCommand(True)
