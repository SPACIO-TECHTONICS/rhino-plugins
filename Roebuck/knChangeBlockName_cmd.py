# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs

__commandname__ = "knChangeBlockName"


def RunCommand(is_interactive):

    block_names = rs.BlockNames()
    if not block_names:
        print("No blocks found in document.")
        return 1

    old_name = rs.ListBox(block_names, "Select block to rename", "Rename Block")
    if not old_name:
        return 1

    new_name = rs.StringBox(
        "Enter new name for block '{}'".format(old_name), old_name, "Rename Block"
    )
    if not new_name or new_name == old_name:
        return 1

    if rs.IsBlock(new_name):
        print("A block with name '{}' already exists.".format(new_name))
        return 1


    import scriptcontext as sc

    idef = sc.doc.InstanceDefinitions.Find(old_name)
    if idef:
        sc.doc.InstanceDefinitions.Modify(idef.Index, new_name, idef.Description, True)
        print("Renamed block '{}' to '{}'".format(old_name, new_name))
        return 0

    return 1


if __name__ == "__main__":
    RunCommand(True)
