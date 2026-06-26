from __future__ import print_function
import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

def RunCommand(is_interactive):


views = Rhino.RhinoDoc.ActiveDoc.Views.GetPageViews()

    print(views)

    for view in views:
        view.SetPageAsActive()
        # Rhino.RhinoDoc.InstanceDefinitions.Find()
        # rs.InsertBlock("STT-A2TitleBlock_PanellingStructure",(0,0,0),(1,1,1))

if __name__ == "__main__":
    RunCommand(True)
