# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# GNU General Public License for more details.
# Copyright (c) 2026 Spacio Techtonics / Keshava Narayan

from __future__ import print_function
import Rhino
import rhinoscriptsyntax as rs

__commandname__ = "knToggleGumballSnap"

def RunCommand( is_interactive ):


    GumSnapState = Rhino.ApplicationSettings.ModelAidSettings.SnappyGumballEnabled
    if GumSnapState:
        Rhino.ApplicationSettings.ModelAidSettings.SnappyGumballEnabled = False
        print('Gumball snap is OFF')
    else:
        Rhino.ApplicationSettings.ModelAidSettings.SnappyGumballEnabled = True
        print('Gumball snap is ON')

if __name__ == "__main__":
    RunCommand(True)
