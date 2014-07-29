"""Kraken - objects.Controls.BaseControl module.

Classes:
BaseControl - Base Control.

"""

from kraken.core.maths.xfo import Xfo
from kraken.core.maths.rotation import Euler
from kraken.core.maths.rotation import Quat
from kraken.core.objects.curve import Curve


class BaseControl(Curve):
    """Base Control object."""

    __kType__ = "Control"

    def __init__(self, name, parent=None):
        """Initializes base control object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(BaseControl, self).__init__(name, parent=parent)

    # =============
    # Name methods
    # =============

    def getBuildName(self):
        """Returns the name used when building the node in the target application.

        Return:
        String, build name of the object.

        """
        
        return super(BaseControl, self).getBuildName() + '_ctrl'

    # ==============
    # Align Methods
    # ==============
    def alignOnXAxis(self, negative=False):
        """Aligns the control shape on the X axis.

        Arguments:
        negative -- Boolean, whether to align the control on the negative X axis.

        Return:
        True if successful.

        """

        furthest = 0.0

        controlPoints = self.copyControlPoints()

        for eachSection in controlPoints:
            for eachPoint in eachSection:

                if negative is False:

                    if eachPoint.x < furthest:
                        furthest = eachPoint.x

                else:

                    if eachPoint.x > furthest:
                        furthest = eachPoint.x


        offset = 0.0 - furthest

        for eachSection in controlPoints:
            for eachPoint in eachSection:
                eachPoint.x += offset

        self.setControlPoints(controlPoints)

        return True


    def alignOnYAxis(self, negative=False):
        """Aligns the control shape on the Y axis.

        Arguments:
        negative -- Boolean, whether to align the control on the negative Y axis.

        Return:
        True if successful.

        """

        furthest = 0.0

        controlPoints = self.copyControlPoints()

        for eachSection in controlPoints:
            for eachPoint in eachSection:

                if negative is False:

                    if eachPoint.y < furthest:
                        furthest = eachPoint.y

                else:

                    if eachPoint.y > furthest:
                        furthest = eachPoint.y


        offset = 0.0 - furthest

        for eachSection in controlPoints:
            for eachPoint in eachSection:
                eachPoint.y += offset

        self.setControlPoints(controlPoints)

        return True


    def alignOnZAxis(self, negative=False):
        """Aligns the control shape on the Z axis.

        Arguments:
        negative -- Boolean, whether to align the control on the negative Z axis.

        Return:
        True if successful.

        """

        furthest = 0.0

        controlPoints = self.copyControlPoints()

        for eachSection in controlPoints:
            for eachPoint in eachSection:

                if negative is False:

                    if eachPoint.z < furthest:
                        furthest = eachPoint.z

                else:

                    if eachPoint.z > furthest:
                        furthest = eachPoint.z


        offset = 0.0 - furthest

        for eachSection in controlPoints:
            for eachPoint in eachSection:
                eachPoint.z += offset

        self.setControlPoints(controlPoints)

        return True


    # ==============
    # Scale Methods
    # ==============
    def scalePoints(self, scaleVec):
        """Scales the point positions from it's center.

        Arguments:
        scaleVec -- Vec3, scale value to apply to the points.

        Return:
        True if successful.

        """

        controlPoints = self.copyControlPoints()

        for eachSection in controlPoints:
            for eachPoint in eachSection:
                eachPoint.x *= scaleVec.x
                eachPoint.y *= scaleVec.y
                eachPoint.z *= scaleVec.z

        self.setControlPoints(controlPoints)

        return True


    # ===============
    # Rotate Methods
    # ===============
    def rotatePoints(self, xRot, yRot, zRot):
        """Rotates the points by the input values.

        Arguments:
        xRot -- Float, euler x rotate value.
        yRot -- Float, euler y rotate value.
        zRot -- Float, euler z rotate value.

        Return:
        True if successful.

        """

        controlPoints = self.copyControlPoints()

        quatRot = Quat()
        quatRot.setFromEuler(Euler(xRot, yRot, zRot))

        newPoints = []
        for eachSection in controlPoints:

            newSectionPoints = []
            for i, eachPoint in enumerate(eachSection):
                eachPoint = quatRot.rotateVector(eachPoint)
                newSectionPoints.append(eachPoint)

            newPoints.append(newSectionPoints)

        self.setControlPoints(newPoints)

        return True


    # ==================
    # Translate Methods
    # ==================
    def translatePoints(self, translateVec):
        """Translates the control points.

        Arguments:
        translateVec -- Vec3, translation values to apply to the points.

        Return:
        True if successful.

        """

        controlPoints = self.copyControlPoints()

        for eachSection in controlPoints:
            for eachPoint in eachSection:
                eachPoint.x += translateVec.x
                eachPoint.y += translateVec.y
                eachPoint.z += translateVec.z

        self.setControlPoints(controlPoints)

        return True