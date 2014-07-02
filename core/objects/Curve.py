"""Kraken - objects.curve module.

Classes:
Curve - Curve.

"""

from kraken.core.objects.scene_item import SceneItem


class Curve(SceneItem):
    """Curve object."""

    def __init__(self, name, parent=None):
        """Initializes the curve object.

        Arguments:
        name -- String, Name of the constraint.
        parent -- Object, parent object of this object.

        """

        super(Curve, self).__init__(name, parent=parent)

        self.controlPoints = []
        self.closed = []


    def getControlPoints(self):
        """Returns the control points of the curve.

        Return:
        Array of Vec3 positions.

        """

        return self.controlPoints


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