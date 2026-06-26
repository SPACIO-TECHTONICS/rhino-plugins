import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore
import random
import Rhino  # type: ignore

sc.doc = Rhino.RhinoDoc.ActiveDoc

__commandname__ = "knRandomColorstoLayers"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):


print("Executing"), __commandname__
    def RandomColorLayers():
        if "CL_Choice" in sc.sticky: sel_choice = sc.sticky["CL_Choice"]
        else: sel_choice = False
        choice=["Select","AllLayers","LayerRange"]
        gb=rs.GetBoolean("Layers to select?",choice,sel_choice)    
        if not gb: return
        if gb[0]:
            layers=rs.GetLayers("Select layers to randomize color")
            if not layers: return
        else:
            layers=rs.LayerNames()
        rs.EnableRedraw(False)
        for layer in layers:
            r=random.randint(0,255)
            g=random.randint(0,255)
            b=random.randint(0,255)
            rs.LayerColor(layer,(r,g,b))
        sc.sticky["CL_Choice"] = sel_choice
    
    RandomColorLayers()

if __name__ == "__main__":
    RunCommand(True)
