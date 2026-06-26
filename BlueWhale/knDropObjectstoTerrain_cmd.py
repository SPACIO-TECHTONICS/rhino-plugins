import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
from assets import auth_helper

__commandname__ = "knDropObjectstoTerrain"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knDropObjectstoTerrain"):
        return auth_helper.get_cancel_result()

    objs = rs.GetObjects('Pick objects to drop', preselect=True)
    if not objs:
        return Rhino.Commands.Result.Cancel
        
    terrain = rs.GetObject("Select terrain surface/mesh", filter=rs.filter.surface | rs.filter.polysurface | rs.filter.mesh)
    if not terrain:
        return Rhino.Commands.Result.Cancel

    rs.EnableRedraw(False)
    try:
        for obj in objs:
            # Simple drop logic: 
            # 1. Get bbox center
            # 2. Project center to terrain
            # 3. Move object to the projected point
            bbox = rs.BoundingBox(obj)
            if not bbox: continue
            
            # Bottom center
            bottom_center = (bbox[0] + bbox[2]) / 2.0
            
            # Project point down onto terrain
            # Using MoveObject logic relative to Z intersection
            # This is a simplification; for complex terrain, users might want to project multiple points.
            pt_on_terrain = rs.ProjectPointToSurface([bottom_center], terrain, [0, 0, -1])
            if not pt_on_terrain:
                # Try projecting up if it's below
                pt_on_terrain = rs.ProjectPointToSurface([bottom_center], terrain, [0, 0, 1])
                
            if pt_on_terrain:
                translation = rs.VectorCreate(pt_on_terrain[0], bottom_center)
                rs.MoveObject(obj, translation)
        
        rs.EnableRedraw(True)
        return Rhino.Commands.Result.Success

    except Exception as e:
        rs.EnableRedraw(True)
        print("Error dropping objects: {0}".format(e))
        return Rhino.Commands.Result.Failure

if __name__ == "__main__":
    RunCommand(True)
