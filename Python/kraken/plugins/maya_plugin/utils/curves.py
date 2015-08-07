from kraken.plugins.maya_plugin.utils import *


def curveToKraken(curve):
    """Converts a curve in Maya to a valid definition for Kraken.

    Args:
        curve (obj): Maya nurbs curve Object.

    Returns:
        list: The curve definition in kraken format.

    """

    shapes = pm.listRelatives(curve, shapes=True)

    data = []
    for eachShape in shapes:
        subCurveData = {
            'points': [[round(y, 3) for y in [x.x, x.y, x.z]] for x in eachShape.getCVs()],
            'degree': eachShape.degree(),
            'closed': eachShape.form() == 'closed'
        }

        data.append(subCurveData)

    return data