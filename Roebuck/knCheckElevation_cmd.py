# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

__commandname__ = "knCheckElevation"


def RunCommand(is_interactive):

    base_elevation = 0.0

    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("Pick point to check elevation")

    optBase = Rhino.Input.Custom.OptionDouble(base_elevation)
    gp.AddOptionDouble("BaseElevation", optBase)

    while True:
        res = gp.Get()

        if res == Rhino.Input.GetResult.Point:
            pt = gp.Point()
            base_elevation = optBase.CurrentValue

            rel_elevation = pt.Z - base_elevation

            unit_system = sc.doc.ModelUnitSystem
            formatted_val = "{:,.3f}".format(rel_elevation)
            result_str = "EL: {} {}".format(formatted_val, str(unit_system).lower())
            print(result_str)
            rs.AddTextDot(result_str, pt)

        elif res == Rhino.Input.GetResult.Option:
            continue
        else:
            break

    return 0


if __name__ == "__main__":
    RunCommand(True)
