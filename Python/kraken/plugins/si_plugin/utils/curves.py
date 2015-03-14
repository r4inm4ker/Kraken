

def curveToKraken(curve):
    """Converts a curve in Softimage to a valid definition for Kraken.

    Arguments:
    curve -- Object, Softimage nurbs curve Object.

    Return:
    String, the curve definition in kraken format.

    """

    crvList = curve.ActivePrimitive.Geometry

    curveSections = []
    curveClosed = []
    for eachCrv in crvList.Curves:

        curvePoints = []
        for eachPnt in eachCrv.ControlPoints:

            points = [round(x, 2) for x in list(eachPnt.Position.Get2())]
            curvePoints.append(points)

        curveSections.append(curvePoints)
        curveClosed.append(eachCrv.Get2()[2])

    krakenOut = "\n"
    for i, eachSection in enumerate(curveSections):

        pointStr = "self.addCurveSection(["

        for eachPoint in eachSection:
            pointStr += "Vec3(" + ", ".join([str(x) for x in eachPoint]) + "), "

        krakenOut += pointStr[:-2] + "], " + str(curveClosed[i]) + ")\n"

    return krakenOut