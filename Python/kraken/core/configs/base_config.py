"""Kraken - base config module.

Classes:
BaseConfig -- Base config object used to configure builders.

"""


class BaseConfig(object):
    """Base Configuration for Kraken builders."""

    _instance = None

    def __init__(self):
        super(BaseConfig, self).__init__()

        # the config is a singleton, so after the first is constructed, throw an error.
        if BaseConfig._instance is not None:
            raise Exception("BaseConfig object constructed twice. Please always call 'BaseConfig.getInstance'")

        BaseConfig._instance = self

        self._explicitNaming = self.initExplicitNaming()
        self._colors = self.initColors()
        self._colorMap = self.initColorMap()
        self._nameTemplate = self.initNameTemplate()
        self._controlShapes = self.initControlShapes()


    # ==============
    # Color Methods
    # ==============
    def initColors(self):
        """Initializes the color values.

        Return:
        Dict, color definitions.

        """

        # Note: These were taken from Maya and is the least common denominator since
        # you can't set colors by scalar values. :\
        #
        # Note 2: Autodesk just implemented this so we need to keep this implementation
        # for a while until it becomes the norm.

        colors = {
                  "black": [1, [0.00, 0.00, 0.0]],
                  "lightGrey": [2, [0.75, 0.75, 0.75]],
                  "darkGrey": [3, [0.50, 0.50, 0.50]],
                  "fusia": [4, [0.80, 0.00, 0.20]],
                  "blueDark": [5, [0.00, 0.00, 0.40]],
                  "blue": [6, [0.00, 0.00, 1.00]],
                  "green": [7, [0.00, 0.30, 0.00]],
                  "purpleDark": [8, [0.20, 0.00, 0.30]],
                  "magenta": [9, [0.80, 0.00, 0.80]],
                  "brownLight": [10, [0.60, 0.30, 0.20]],
                  "brownDark": [11, [0.25, 0.13, 0.13]],
                  "orange": [12, [0.70, 0.20, 0.00]],
                  "red": [13, [1.00, 0.00, 0.00]],
                  "greenBright": [14, [0.00, 1.00, 0.00]],
                  "blueMedium": [15, [0.00, 0.30, 0.60]],
                  "white": [16, [1.00, 1.00, 1.00]],
                  "yellow": [17, [1.00, 1.00, 0.00]],
                  "greenBlue": [18, [0.00, 1.00, 1.00]],
                  "turqoise": [19, [0.00, 1.00, 0.80]],
                  "pink": [20, [1.00, 0.70, 0.70]],
                  "peach": [21, [0.90, 0.70, 0.50]],
                  "yellowLight": [22, [1.00, 1.00, 0.40]],
                  "turqoiseDark": [23, [0.00, 0.70, 0.40]],
                  "brownMuted": [24, [0.60, 0.40, 0.20]],
                  "yellowMuted": [25, [0.63, 0.63, 0.17]],
                  "greenMuted": [26, [0.40, 0.60, 0.20]],
                  "turqoiseMuted": [27, [0.20, 0.63, 0.35]],
                  "blueLightMuted": [28, [0.18, 0.63, 0.63]],
                  "blueDarkMuted": [29, [0.18, 0.40, 0.63]],
                  "purpleLight": [30, [0.43, 0.18, 0.63]],
                  "mutedMagenta": [31, [0.63, 0.18, 0.40]]
                 }

        return colors


    def getColors(self):
        """Gets the colors defined in the config.

        Return:
        Dict, colors.

        """

        return self._colors


    # ======================
    # Color Mapping Methods
    # ======================
    def initColorMap(self):
        """Initializes the color values.

        Return:
        Dict, color definitions.

        """

        colorMap = {
                    "Control": {
                                "default": "yellow",
                                "L": "greenBright",
                                "M": "yellow",
                                "R": "red"
                               }
                   }

        return colorMap


    def getColorMap(self):
        """Gets the color map defined in the config.

        Return:
        Dict, color map.

        """

        return self._colorMap


    # ======================
    # Name Template Methods
    # ======================
    def initNameTemplate(self):
        """Initializes the name template.

        Return:
        Dict, name template.

        """

        nameTemplate = {
                        "locations": ["L", "R", "M"],
                        "mirrorMap": {
                                      "L": "R",
                                      "R": "L",
                                      "M": "M"
                                     },
                        "separator": "_",
                        "types": {
                                  "default": "null",
                                  "Component": "cmp",
                                  "ComponentInput": "cmpIn",
                                  "ComponentOutput": "cmpOut",
                                  "Container": "",
                                  "Control": "ctrl",
                                  "Curve": "crv",
                                  "HierarchyGroup": "hrc",
                                  "Joint": "def",
                                  "Layer": "",
                                  "Locator": "loc",
                                  "SrtBuffer": "srtBuffer"
                                 },
                        "formats":
                                  {
                                   "Container": ["name"],
                                   "Layer": ["name"],
                                   "Component": ["name", "sep", "location", "sep", "type"],
                                   "default": ["component", "sep", "location", "sep", "name", "sep", "type"],
                                  }
                       }

        return nameTemplate


    def getNameTemplate(self):
        """Returns the naming template for this configuration.

        Return:
        Dict, naming template.

        """

        return self._nameTemplate


    # ======================
    # Control Shape Methods
    # ======================
    def initControlShapes(self):
        """Doc String.

        Arguments:
        Arguments -- Type, information.

        Return:
        True if successful.

        """

        controlShapes = {
                         "arrow": [
                                   {
                                    "points": [
                                               [-0.05, 0.0, -0.25],
                                               [-0.15, 0.0, -0.25],
                                               [0.0, -0.0, -0.5],
                                               [0.15, 0.0, -0.25],
                                               [0.05, 0.0, -0.25],
                                               [0.05, 0.0, 0.5],
                                               [-0.05, 0.0, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   }
                                  ],
                         "arrows": [
                                    {
                                     "points": [
                                                [-0.05, 0.0, 0.05],
                                                [-0.05, 0.0, 0.25],
                                                [-0.15, 0.0, 0.25],
                                                [0.0, -0.0, 0.4],
                                                [0.15, 0.0, 0.25],
                                                [0.05, 0.0, 0.25],
                                                [0.05, 0.0, 0.05],
                                                [0.25, 0.0, 0.05],
                                                [0.25, 0.0, 0.15],
                                                [0.4, -0.0, 0.0],
                                                [0.25, 0.0, -0.15],
                                                [0.25, 0.0, -0.05],
                                                [0.05, 0.0, -0.05],
                                                [0.05, 0.0, -0.25],
                                                [0.15, 0.0, -0.25],
                                                [0.0, -0.0, -0.4],
                                                [-0.15, 0.0, -0.25],
                                                [-0.05, 0.0, -0.25],
                                                [-0.05, 0.0, -0.05],
                                                [-0.25, 0.0, -0.05],
                                                [-0.25, 0.0, -0.15],
                                                [-0.4, -0.0, -0.0],
                                                [-0.25, 0.0, 0.15],
                                                [-0.25, 0.0, 0.05]
                                               ],
                                     "degree": 1,
                                     "closed": True
                                    }
                                   ],
                         "circle": [
                                    {
                                     "points": [
                                                [0.35, 0.0, -0.35],
                                                [0.5, 0.0, 0.0],
                                                [0.35, 0.0, 0.35],
                                                [0.0, 0.0, 0.5],
                                                [-0.35, 0.0, 0.35],
                                                [-0.5, 0.0, 0.0],
                                                [-0.35, 0.0, -0.35],
                                                [0.0, 0.0, -0.5]
                                               ],
                                     "degree": 1,
                                     "closed": True
                                    }
                                   ],
                         "cube": [
                                   {
                                    "points": [
                                               [-0.5, -0.5, -0.5],
                                               [-0.5, 0.5, -0.5],
                                               [0.5, 0.5, -0.5],
                                               [0.5, -0.5, -0.5]
                                              ],
                                    "degree": 1,
                                    "closed": True
                                   },
                                   {
                                    "points": [
                                               [-0.5, -0.5, 0.5],
                                               [-0.5, 0.5, 0.5],
                                               [0.5, 0.5, 0.5],
                                               [0.5, -0.5, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": True
                                   },
                                   {
                                    "points": [
                                               [-0.5, -0.5, -0.5],
                                               [-0.5, -0.5, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   },
                                   {
                                    "points": [
                                               [0.5, -0.5, -0.5],
                                               [0.5, -0.5, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   },
                                   {
                                    "points": [
                                               [-0.5, 0.5, -0.5],
                                               [-0.5, 0.5, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   },
                                   {
                                    "points": [
                                               [0.5, 0.5, -0.5],
                                               [0.5, 0.5, 0.5]
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   }
                                  ],
                         "null": [
                                  {
                                   "points": [
                                              [-0.5, 0.0, 0.0],
                                              [0.5, 0.0, 0.0]
                                             ],
                                   "degree": 1,
                                   "closed": False
                                  },
                                  {
                                   "points": [
                                              [0.0, -0.5, 0.0],
                                              [0.0, 0.5, 0.0]
                                             ],
                                   "degree": 1,
                                   "closed": False
                                  },
                                  {
                                   "points": [
                                              [0.0, 0.0, -0.5],
                                              [0.0, 0.0, 0.5]
                                             ],
                                   "degree": 1,
                                   "closed": False
                                  }
                                 ],
                         "pin": [
                                 {
                                  "points": [
                                             [0.0, 0.0, -0.5],
                                             [-0.17, 0.0, -0.57],
                                             [-0.25, 0.0, -0.75],
                                             [-0.17, 0.0, -0.93],
                                             [0.0, 0.0, -1.0],
                                             [0.17, 0.0, -0.93],
                                             [0.25, 0.0, -0.75],
                                             [0.17, 0.0, -0.57],
                                             [0.0, 0.0, -0.5],
                                             [0.0, 0.0, 0.0]
                                            ],
                                  "degree": 1,
                                  "closed": False
                                 }
                                ],
                         "sphere": [
                                    {
                                     "points": [
                                                [0.0, 0.5, 0.0],
                                                [0.0, 0.35, -0.35],
                                                [0.0, 0.0, -0.5],
                                                [0.0, -0.35, -0.35],
                                                [0.0, -0.5, 0.0],
                                                [0.0, -0.35, 0.35],
                                                [0.0, 0.0, 0.5],
                                                [0.0, 0.35, 0.35]
                                               ],
                                     "degree": 1,
                                     "closed": True
                                    },
                                    {
                                     "points": [
                                                [0.0, 0.0, -0.5],
                                                [0.35, 0.0, -0.35],
                                                [0.5, 0.0, 0.0],
                                                [0.35, 0.0, 0.35],
                                                [0.0, 0.0, 0.5],
                                                [-0.35, 0.0, 0.35],
                                                [-0.5, 0.0, 0.0],
                                                [-0.35, 0.0, -0.35]
                                               ],
                                     "degree": 1,
                                     "closed": True
                                    },
                                    {
                                     "points": [
                                                [0.0, 0.5, 0.0],
                                                [0.35, 0.35, 0.0],
                                                [0.5, 0.0, 0.0],
                                                [0.35, -0.35, 0.0],
                                                [0.0, -0.5, 0.0],
                                                [-0.35, -0.35, 0.0],
                                                [-0.5, 0.0, 0.0],
                                                [-0.35, 0.35, 0.0]
                                               ],
                                     "degree": 1,
                                     "closed": True
                                    }
                                   ],
                         "square": [
                                    {
                                     "points": [
                                                [0.5, 0.0, -0.5],
                                                [0.5, 0.0, 0.5],
                                                [-0.5, 0.0, 0.5],
                                                [-0.5, 0.0, -0.5]
                                               ],
                                     "degree": 1,
                                     "closed": False
                                    }
                                   ],
                         "triangle": [
                                      {
                                       "points": [
                                                  [0.0,0.0,-0.5],
                                                  [-0.5,0.0,0.5],
                                                  [0.5,0.0,0.5]
                                                 ],
                                       "degree": 1,
                                       "closed": True
                                      }
                                     ]
                        }

        return controlShapes


    def getControlShapes(self):
        """Returns the control shapes for this configuration.

        Return:
        Dict, control shapes.

        """

        return self._controlShapes


    # =========================
    # Explicity Naming Methods
    # =========================
    def initExplicitNaming(self):
        """Returns the value of the explicit naming attribute.

        Return:
        Boolean, initial value for explicit naming.

        """

        return False


    def getExplicitNaming(self):
        """Returns the value of the explicit naming attribute.

        Return:
        Boolean, current value.

        """

        return self._explicitNaming


    def setExplicitNaming(self, value):
        """Set the config to use explicit naming.

        Arguments:
        value -- Boolean, whether to use explicit naming or not.

        Return:
        True if successful.

        """

        self._explicitNaming = value

        return True


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getInstance(cls):
        """This class method returns the singleton instance for the BaseConfig.

        Return:
        The singleton instance.

        """

        if BaseConfig._instance is None:
            cls()
        elif not isinstance(BaseConfig._instance, BaseConfig):
            raise Exception("Multiple different BaseConfig types have been constructed.");

        return BaseConfig._instance


    def clearInstance(cls):
        """Clears the instance variable of the config.

        Return:
        True if successful.

        """

        BaseConfig._instance = None

        return True