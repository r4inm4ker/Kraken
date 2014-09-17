"""Kraken - base config module.

Classes:
BaseConfig -- Base config object used to configure builders.

"""


class BaseConfig(object):
    """Base Configuration for Kraken builders."""

    def __init__(self):
        super(BaseConfig, self).__init__()

        self.nameTemplate = {
                             "sides": ['L', 'R', 'M'],
                             "separator": "_",
                             "types": {
                                       "default": "null",
                                       "Control": "ctrl",
                                       "Null": "null"
                                      },
                             "formats":
                                       {
                                        "default": ['component', 'sep', 'side', 'sep', 'name', 'sep', 'type'],
                                        "Rig": ['name'],
                                        "Layer": ['name']
                                       }
                            }


    def getNameTemplate(self):
        """Returns the naming template for this configuration.

        Return:
        Dict, naming template.

        """

        return self.nameTemplate