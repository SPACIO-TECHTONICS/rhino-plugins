# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

import rhinoscriptsyntax as rs

__commandname__ = "knSelAllGroups"

def RunCommand( is_interactive ):


    gnames = rs.GroupNames()
    
    for name in gnames:
        rs.Command("-SelGroup " + name)

if __name__ == "__main__":
    RunCommand(True)



