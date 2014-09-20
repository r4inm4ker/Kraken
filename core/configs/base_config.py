"""Kraken - base config module.

Classes:
BaseConfig -- Base config object used to configure builders.

"""


class BaseConfig(object):
    """Base Configuration for Kraken builders."""

    def __init__(self):
        super(BaseConfig, self).__init__()

        self.nameTemplate = {
                             "locations": ['L', 'R', 'M'],
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
                                       "Locator": "null",
                                       "SrtBuffer": "srtBuffer"
                                      },
                             "formats":
                                       {
                                        "default": ['component', 'sep', 'location', 'sep', 'name', 'sep', 'type'],
                                        "Container": ['name'],
                                        "Layer": ['name'],
                                        "Component": ['name', 'sep', 'location', 'sep', 'type']
                                       }
                            }


    def getNameTemplate(self):
        """Returns the naming template for this configuration.

        Return:
        Dict, naming template.

        """

        return self.nameTemplate