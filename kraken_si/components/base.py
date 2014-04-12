"""Kraken - Softimage - objects.elements module.

Classes:
Scene -- Scene root representation.
Group -- Object used to group objects together.
Null -- Basic 3d transform with basic graphical representation.
Asset -- Namespace object.

"""

import json

from kraken.core.components import base
from kraken.kraken_si.utils import *
from kraken.kraken_si.objects import elements


class BaseComponent(base.BaseComponent, elements.Group):
    """Base rigging component."""

    def __init__(self, name, side="M", parent=None):
        """Initializes base component.

        Arguments:
        name -- String, Name of component.
        side -- String, location of the component.
        parent -- Object, parent object of this component.

        Keyword Arguments:
        parent -- Object, Parent object to create object under.

        """

        super(BaseComponent, self).__init__(name, side=side, parent=parent)
        self.app = "si"


    # ==========================
    # Component Build Functions
    # ==========================
    def _preBuild(self):
        """Pre-build operations.

        Return:
        True if successful.

        """

        super(BaseComponent, self)._preBuild()

        return True


    def _build(self):
        """Builds element in Softimage.

        NOTE: When building the component, remember that you should create / add
        objects in the order of IO Hrc, Ctrl Hrc, and Armature Hrc.

        Return:
        3D Object in Softimage.

        """

        super(BaseComponent, self)._build()

        # Setup component hierarchy
        elements.Group(self.name.split("_")[0] + "_io_hrc", parent=self)
        elements.Group(self.name.split("_")[0] + "_ctrl_hrc", parent=self)
        elements.Group(self.name.split("_")[0] + "_armature_hrc", parent=self)

        return True


    def _postBuild(self):
        """Post-build operations.

        Return:
        True if successful.

        """

        super(BaseComponent, self)._postBuild()

        return True