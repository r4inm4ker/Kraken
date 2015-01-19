"""Kraken - objects.curve module.

Classes:
Curve - Curve.

"""

from kraken.core.objects.scene_item import SceneItem

import copy


class Curve(SceneItem):
    """Curve object."""

    __kType__ = "Curve"

    def __init__(self, name, parent=None):
        super(Curve, self).__init__(name, parent=parent)

        self.controlPoints = []
        self.closed = []


    # ======================
    # Control Point Methods
    # ======================
    def setControlPoints(self, points):
        """Sets the control points array.

        Arguments:
        points -- List, 2D array of Vec3 points to describe the curve's shape.

        Return:
        True if successful.

        """

        self.controlPoints = points

        return True


    def getControlPoints(self):
        """Returns the control points of the curve.

        Return:
        Array of Vec3 positions.

        """

        return self.controlPoints


    def copyControlPoints(self):
        """Returns the control points of the curve.

        Return:
        Array of Vec3 positions.

        """

        # return copy.deepcopy(self.controlPoints)
        return self.controlPoints


    def appendControlPoints(self, points):
        """Appends control points to the current curve.

        Arguments:
        points -- List, 1D array of Vec3 points to add to the curve description.

        Return:
        True if successful.

        """

        self.controlPoints.append(points)

        return True


    # ======================
    # Curve Section Methods
    # ======================
    def checkSectionIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, section index to check.

        """

        if index > len(self.controlPoints):
            raise IndexError("'" + str(index) + "' is out of the range of the 'controlPoints' array.")

        return True


    def addCurveSection(self, controlPoints, closed=False):
        """Sets the control points of the control.

        Arguments:
        controlPoints -- Array, array of Vec3 objects of point positions.
        closed -- Boolean, whether the sub-curve is closed or not.

        Return:
        True if successful.

        """

        self.controlPoints.append(controlPoints)
        self.closed.append(closed)

        return True


    def getNumCurveSections(self):
        """Returns the number of curve sections on this object.

        Return:
        Integner, number of curve sections in this object.

        """

        return len(self.controlPoints)


    def getCurveSectionClosed(self, index):
        """Returns whether the curve section is closed or not.

        Arguments:
        index -- Integer, index of the curve section to query.

        Return:
        True or False if the section is closed.

        """

        if self.checkSectionIndex(index) is not True:
            return False

        return self.closed[index]


    def setCurveSectionArray(self, index, array):
        """Get the curve section array by it's index.

        Arguments:
        index -- Integer, index of the section to get the array for.

        Return:
        True if successful.

        """

        if self.checkSectionIndex(index) is not True:
            return False

        self.controlPoints[index] = array

        return True


    def getCurveSectionArray(self, index):
        """Get the curve section array by it's index.

        Arguments:
        index -- Integer, index of the section to get the array for.

        Return:
        Array, Vec3 values for that section of the curve.

        """

        if self.checkSectionIndex(index) is not True:
            return False

        return self.controlPoints[index]

        return


    def removeCurveSectionByIndex(self, index):
        """Removes a curve section by its index.

        Arguments:
        index -- Integer, Index of the section to remove.

        Return:
        True if successful.

        """

        if self.checkSectionIndex(index) is not True:
            return False

        del self.controlPoints[index]

        return True