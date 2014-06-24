"""Kraken - objects.Control module.

Classes:
Control - Control Object.

"""


import SceneItem

class Control(SceneItem):
    """Kraken Control Object"""

    def __init__(self, name, parent=None):
        super(Control, self).__init__(name, parent)
        self.name = name
        self.parent = parent