from __future__ import print_function
import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

__commandname__ = "knToggleGumballSnap"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
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
