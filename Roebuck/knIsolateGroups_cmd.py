import rhinoscriptsyntax as rs  # type: ignore
import Rhino as r  # type: ignore



__commandname__ = "knIsolateGroups"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


gnames = rs.GroupNames()
    
    for name in gnames:
        rs.Command("-SelGroup " + name)
    
    rs.Command("Isolate")

if __name__ == "__main__":
    RunCommand(True)
