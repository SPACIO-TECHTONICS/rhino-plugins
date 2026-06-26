import rhinoscriptsyntax as rs  # type: ignore
import Rhino  # type: ignore
from assets import auth_helper
from assets import osm_utilities

__commandname__ = "knCurveBooleanUnion"

def RunCommand(is_interactive):
    if not auth_helper.ensure_authenticated("BlueWhale", "knCurveBooleanUnion"):
        return auth_helper.get_cancel_result()

    srf_ids = rs.GetObjects("Select Surfaces to union", rs.filter.surface)
    if not srf_ids:
        return Rhino.Commands.Result.Cancel

    curve_ids = []
    for srf in srf_ids:
        curve_ids.extend(rs.DuplicateSurfaceBorder(srf))

    if curve_ids and len(curve_ids) > 1:
        try:
            result = rs.CurveBooleanUnion(curve_ids)
            if result:
                osm_utilities.CreatePlanarSrfsfromCurves(result)
                rs.DeleteObjects(curve_ids)
                rs.DeleteObjects(srf_ids)
                return Rhino.Commands.Result.Success
            else:
                print("Curve boolean union failed.")
                return Rhino.Commands.Result.Failure
        except Exception as e:
            print("Error during curve boolean union: {0}".format(e))
            return Rhino.Commands.Result.Failure
    else:
        print("Not enough curves to perform union.")
        return Rhino.Commands.Result.Nothing

if __name__ == "__main__":
    RunCommand(True)
