

def curveToKraken(curve):
    """Converts a curve in Softimage to a valid definition for Kraken.

    Args:
        curve (obj): Softimage nurbs curve Object.

    Returns:
        list: The curve definition in kraken format.

    """

    crvList = curve.ActivePrimitive.Geometry

    data = []
    for eachCrv in crvList.Curves:
        subCurveData = {
            'points': [[round(y, 3) for y in list(x.Position.Get2())] for x in eachCrv.ControlPoints],
            'degree': eachCrv.Degree,
            'closed': eachCrv.Get2()[2]
        }

        data.append(subCurveData)

    return data