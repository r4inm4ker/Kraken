"""Kraken - objects.curve module.

Classes:
Curve - Curve.

"""

import copy

from kraken.core.objects.object_3d import Object3D


class Curve(Object3D):
    """Curve object."""

    def __init__(self, name, parent=None):
        super(Curve, self).__init__(name, parent=parent)

        self._data = None


    # ======================
    # Control Point Methods
    # ======================
    def getCurveData(self):
        """Returns the data of the curve.

        Return:
        List, dictionaries defining each sub-curve of this curve.

        """

        return self._data


    def setCurveData(self, data):
        """Sets the curve data.

        Arguments:
        data -- List, dictionaries defining each sub-curve of this curve.

        Return:
        True if successful.

        """

        self._data = copy.deepcopy(data)

        return True


    def appendCurveData(self, data):
        """Appends sub-curve data to this curve.

        Arguments:
        data -- List, dictionaries defining each sub-curve being added to this
        curve.

        Return:
        True if successful.

        """

        self._data += data

        return True


    # ==================
    # Sub-Curve Methods
    # ==================
    def checkSubCurveIndex(self, index):
        """Checks the supplied index is valid.

        Arguments:
        index -- Integer, sub-curve index to check.

        """

        if index > len(self.getCurveData()):
            raise IndexError("'" + str(index) + "' is out of the range of the 'data' array.")

        return True


    def getNumSubCurves(self):
        """Returns the number of sub-curves on this object.

        Return:
        Integer, number of sub-curves in this object.

        """

        return len(self.getCurveData())


    def getSubCurveClosed(self, index):
        """Returns whether the sub-curve is closed or not.

        Arguments:
        index -- Integer, index of the sub-curve to query.

        Return:
        True or False if the sub-curve is closed.

        """

        if self.checkSubCurveIndex(index) is not True:
            return False

        return self._data[index]["closed"]


    def getSubCurveData(self, index):
        """Get the sub-curve data by it's index.

        Arguments:
        index -- Integer, index of the sub-curve to get the data for.

        Return:
        Dict, data defining the sub-curve.

        """

        if self.checkSubCurveIndex(index) is not True:
            return False

        return self._data[index]


    def setSubCurveData(self, index, data):
        """Sets the sub-curve data.

        Arguments:
        index -- Integer, index of the sub-curve to get the data for.
        data -- Dict, defining the sub-curve data.

        Return:
        True if successful.

        """

        if self.checkSubCurveIndex(index) is not True:
            return False

        self._data[index] = data

        return True


    def removeSubCurveByIndex(self, index):
        """Removes a sub-curve by its index.

        Arguments:
        index -- Integer, Index of the sub-curve to remove.

        Return:
        True if successful.

        """

        if self.checkSubCurveIndex(index) is not True:
            return False

        del self._data[index]

        return True
