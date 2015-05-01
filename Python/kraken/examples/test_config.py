from kraken.core.configs.config import Config


class TestConfig(Config):
    """Test configuration."""

    def __init__(self):
        super(TestConfig, self).__init__()


    def initColorMap(self):
        """Initializes the color values.

        Return:
        Dict, color definitions.

        """

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


    def initColorMap(self):
        """Initializes the color values.

        Return:
        Dict, color definitions.

        """

        colorMap = {
                    "Control": {
                                "default": "green",
                                "L": "turqoise",
                                "M": "orange",
                                "R": "magenta"
                               }
                   }

        return colorMap


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
                                  "default": "nl",
                                  "BaseComponent": "cp",
                                  "ComponentInput": "cpIn",
                                  "ComponentOutput": "cpOut",
                                  "Container": "con",
                                  "Control": "con",
                                  "Curve": "crve",
                                  "HierarchyGroup": "sec",
                                  "Joint": "env",
                                  "Layer": "",
                                  "Locator": "nl",
                                  "SrtBuffer": "zero"
                                 },
                        "formats":
                                  {
                                   "default": ["location", "sep", "component", "sep", "name", "sep", "type"],
                                   "Container": ["name"],
                                   "Layer": ["name"],
                                   "BaseComponent": ["location", "sep", "name", "sep", "type"]
                                  }
                       }

        return nameTemplate
