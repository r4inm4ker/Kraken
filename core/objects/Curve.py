"""Kraken - objects.Curve module.

Classes:
Curve - Curve.

"""

from kraken.core.objects.scene_item import SceneItem


class Curve(SceneItem):
    """Curve object."""

    def __init__(self, name, parent=None, controlPoints=None, closed=False):
        """Initializes the curve object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.
        controlPoints -- Array, of x, y, z values of point positions.

        """

        super(Curve, self).__init__(name, parent=parent)
        self.controlPoints = controlPoints
        self.closed = closed


    def setClosed(self, closed):
        """Sets whether the curve is open or closed.

        Arguments:
        closed -- Boolean, closed of whether the curve is open or closed.

        Return:
        True if successful.

        """

        self.closed = closed

        return True


    def getControlPoints(self):
        """Returns the control points."""

        return self.controlPoints


    def setControlPoints(self, controlPoints):
      """Sets the control points of the control.

      Arguments:
      controlPoints -- Array, of x, y, z values of point controlPoints.

      Return:
      True if successful.

      """

      self.controlPoints = controlPoints

      return True