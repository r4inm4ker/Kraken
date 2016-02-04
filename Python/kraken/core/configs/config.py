"""Kraken - base config module.

Classes:
Config -- Base config object used to configure builders.

"""


class Config(object):
    """Base Configuration for Kraken builders."""

    __instance = None

    def __init__(self):
        super(Config, self).__init__()

        # the config is a singleton, so after the first is constructed, throw an error.
        if Config.__instance is not None:
            raise Exception("Config object constructed twice. Please always call 'Config.getInstance'")

        Config.__instance = self

        self._explicitNaming = False
        self._colors = self.initColors()
        self._colorMap = self.initColorMap()
        self._nameTemplate = self.initNameTemplate()
        self._controlShapes = self.initControlShapes()


    # ==============
    # Color Methods
    # ==============
    def initColors(self):
        """Initializes the color values.

        Returns:
            dict: color definitions.

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

        Returns:
            dict: colors.

        """

        return self._colors


    # ======================
    # Color Mapping Methods
    # ======================
    def initColorMap(self):
        """Initializes the color values.

        Returns:
            dict: color definitions.

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

        Returns:
            dict: color map.

        """

        return self._colorMap


    # ======================
    # Name Template Methods
    # ======================
    def initNameTemplate(self):
        """Initializes the name template.

        Returns:
            dict: name template.

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
                                  "Component": "",
                                  "ComponentGroup": "cmp",
                                  "ComponentInput": "cmpIn",
                                  "ComponentOutput": "cmpOut",
                                  "Container": "",
                                  "Control": "ctrl",
                                  "Curve": "crv",
                                  "HierarchyGroup": "hrc",
                                  "Joint": "def",
                                  "Layer": "",
                                  "Locator": "loc",
                                  "CtrlSpace": "ctrlSpace"
                                 },
                        "formats":
                                  {
                                   "Container": ["name"],
                                   "Layer": ["container", "sep", "name"],
                                   "ComponentGroup": ["name", "sep", "location", "sep", "type"],
                                   "default": ["component", "sep", "location", "sep", "name", "sep", "type"],
                                  }
                       }

        return nameTemplate


    def getNameTemplate(self):
        """Returns the naming template for this configuration.

        Returns:
            dict: naming template.

        """

        return self._nameTemplate


    # ======================
    # Control Shape Methods
    # ======================
    def initControlShapes(self):
        """Initializes the control shapes.

        Returns:
            bool: True if successful.

        """

        controlShapes = {
                         "point": [
                                   {
                                    "points": [
                                               [0.0, 0.0, 0.0],
                                              ],
                                    "degree": 1,
                                    "closed": False
                                   }
                                  ],
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
                         "axes": [
                                  {
                                   "points": [
                                              [0.0, 0.0, 0.0],
                                              [0.5, 0.0, 0.0]
                                             ],
                                   "closed": False,
                                   "degree": 1
                                  },
                                  {
                                   "points": [
                                              [0.0, 0.5, 0.0],
                                              [0.0, 0.0, 0.0]
                                             ],
                                   "closed": False,
                                   "degree": 1
                                  },
                                  {
                                   "points": [
                                              [0.0, 0.0, 0.0],
                                              [0.0, 0.0, 0.5]
                                             ],
                                   "closed": False,
                                   "degree": 1}
                                   ],
                         "axesHalfTarget": [
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [0.5, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.5, 0.0],
                                                    [0.0, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [0.0, 0.0, 0.5]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [-0.5, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [-0.25, 0.0, 0.0],
                                                    [-0.25, 0.066, 0.0],
                                                    [-0.196, 0.195, 0.0],
                                                    [0.0, 0.277, 0.0],
                                                    [0.196, 0.195, 0.0],
                                                    [0.25, 0.066, 0.0],
                                                    [0.25, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 3
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [0.5, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.5, 0.0],
                                                    [0.0, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [0.0, 0.0, 0.5]],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [0.0, 0.0, 0.0],
                                                    [-0.5, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 1
                                        },
                                        {
                                         'points': [
                                                    [-0.25, 0.0, 0.0],
                                                    [-0.25, 0.066, 0.0],
                                                    [-0.196, 0.195, 0.0],
                                                    [0.0, 0.277, 0.0],
                                                    [0.196, 0.195, 0.0],
                                                    [0.25, 0.066, 0.0],
                                                    [0.25, 0.0, 0.0]
                                                   ],
                                         'closed': False,
                                         'degree': 3
                                         },
                                         {
                                          'points': [
                                                     [0.0, 0.25, 0.0],
                                                     [0.0, 0.25, 0.033],
                                                     [0.0, 0.237, 0.098],
                                                     [0.0, 0.181, 0.181],
                                                     [0.0, 0.098, 0.237], [0.0, 0.033, 0.25], [0.0, 0.0, 0.25]
                                                    ],
                                          'closed': False,
                                          'degree': 3
                                         },
                                         {
                                          'points': [
                                                     [0.25, 0.0, 0.0],
                                                     [0.25, 0.0, 0.033],
                                                     [0.237, 0.0, 0.098],
                                                     [0.181, 0.0, 0.181],
                                                     [0.098, -0.0, 0.237],
                                                     [0.033, -0.0, 0.25],
                                                     [0.0, -0.0, 0.25]
                                                    ],
                                          'closed': False,
                                          'degree': 3
                                         },
                                         {
                                          'points': [
                                                     [-0.25, 0.0, 0.0],
                                                     [-0.25, 0.0, 0.033],
                                                     [-0.237, 0.0, 0.098],
                                                     [-0.181, 0.0, 0.181],
                                                     [-0.098, 0.0, 0.237],
                                                     [-0.033, 0.0, 0.25],
                                                     [0.0, 0.0, 0.25]
                                                    ],
                                          'closed': False,
                                          'degree': 3
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
                                     "closed": True
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
                                     ],
                         "fkCircle": [
                                      {
                                       "points": [
                                                  [0.0, 0.35, -0.35],
                                                  [0.0, 0.46, -0.09],
                                                  [0.0, 0.55, 0.0],
                                                  [0.0, 0.46, 0.09],
                                                  [0.0, 0.35, 0.35],
                                                  [0.0, 0.09, 0.46],
                                                  [0.0, 0.0, 0.55],
                                                  [-0.0, -0.09, 0.46],
                                                  [-0.0, -0.35, 0.35],
                                                  [-0.0, -0.5, 0.0],
                                                  [-0.0, -0.35, -0.35],
                                                  [0.0, 0.0, -0.5]
                                                 ],
                                        "degree": 1,
                                        "closed": True
                                       },
                                       {
                                        "points": [
                                                   [0.0, 0.0, 0.0],
                                                   [1.0, 0.0, 0.0]
                                                  ],
                                        "degree": 1,
                                        "closed": False
                                       }
                                     ],
                         "vertebra": [
                                      {
                                       "points": [
                                                  [-0.5, -0.0, -0.5],
                                                  [0.5, 0.0, -0.5],
                                                  [0.25, 0.0, 0.5],
                                                  [-0.25, -0.0, 0.5]
                                                 ],
                                       "closed": True,
                                       "degree": 1
                                      },
                                      {
                                       "points": [
                                                  [0.0, 0.0, -0.5],
                                                  [0.0, 0.5, -0.5],
                                                  [0.0, 0.25, 0.5],
                                                  [0.0, 0.0, 0.5]
                                                 ],
                                       "closed": True,
                                       "degree": 1
                                      }
                                     ]
                        }

        return controlShapes


    def getControlShapes(self):
        """Returns the control shapes for this configuration.

        Returns:
            dict: control shapes.

        """

        return self._controlShapes


    # =========================
    # Explicity Naming Methods
    # =========================
    def getExplicitNaming(self):
        """Returns the value of the explicit naming attribute.

        Returns:
            bool: current value.

        """

        return self._explicitNaming


    def setExplicitNaming(self, value):
        """Set the config to use explicit naming.

        Args:
            value (bool): whether to use explicit naming or not.

        Returns:
            bool: True if successful.

        """

        self._explicitNaming = value

        return True


    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getInstance(cls):
        """This class method returns the singleton instance for the Config.

        Returns:
            object: The singleton config instance.

        """

        if Config.__instance is None:
            cls()
        elif not isinstance(Config.__instance, Config):
            raise Exception("Multiple different Config types have been \
                            constructed.")

        return Config.__instance


    @classmethod
    def makeCurrent(cls):
        """Sets this class t be the singleton instance Config.

        Returns:
            object: The singleton config instance.

        """

        Config.__instance = None
        Config.__instance = cls()


    @classmethod
    def clearInstance(cls):
        """Clears the instance variable of the config.

        Returns:
            bool: True if successful.

        """

        Config.__instance = None

        return True

