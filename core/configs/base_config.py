"""Kraken - base config module.

Classes:
BaseConfig -- Base config object used to configure builders.

"""


class BaseConfig(object):
    """Base Configuration for Kraken builders."""

    def __init__(self):
        super(BaseConfig, self).__init__()

        # Note: These were taken from Maya and is the least common denominator since
        # you can't set colors by scalar values. :\
        #
        # Note 2: Autodesk just implemented this so we need to keep this implementation
        # for a while until it becomes the norm.

        self.colors = {
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

        self.colorMap = {
                         "Control": {
                                     "default": "yellow",
                                     "L": "greenBright",
                                     "M": "yellow",
                                     "R": "red"
                                    },
                        }

        self.nameTemplate = {
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
                                        "default": ["component", "sep", "location", "sep", "name", "sep", "type"],
                                        "Container": ["name"],
                                        "Layer": ["name"],
                                        "Component": ["name", "sep", "location", "sep", "type"]
                                       }
                            }

    # ==============
    # Color Methods
    # ==============
    def getColors(self):
        """Gets the colors defined in the config.

        Arguments:
        Arguments -- Type, information.

        Return:
        Dict, colors.

        """

        return self.colors


    # ======================
    # Name Template Methods
    # ======================
    def getNameTemplate(self):
        """Returns the naming template for this configuration.

        Return:
        Dict, naming template.

        """

        return self.nameTemplate


    # ===================
    # Validation Methods
    # ===================
    def validateConfig(self):
        """Validates the configuration.

        Return:
        True if valid.

        """

        # TODO: check colorMap locations are valid locations
        # TODO: check colorMap types are valid types
        # TODO: check colorMap type entries have a 'default' value.

        return True