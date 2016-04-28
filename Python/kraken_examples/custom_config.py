

from kraken.core.configs.config import Config

class CustomConfig(Config):
    """Custom Config Example.

    This demonstrates to users how they can customize only the name template
    portion of a Config when sub-classed off of the base Config.

    """

    def __init__(self):
        super(CustomConfig, self).__init__()

    # ======================
    # Name Template Methods
    # ======================
    def initNameTemplate(self):
        """Initializes the name template.

        Returns:
            dict: name template.

        """

        nameTemplate = super(CustomConfig, self).initNameTemplate()
        nameTemplate["formats"] =  {
                                   "Container": ["name"],
                                   "Layer": ["container", "sep", "name"],
                                   "ComponentGroup": ["location", "sep", "name", "sep", "type"],
                                   "default": ["location", "sep", "component", "sep", "name", "sep", "type"],
                                  }

        return nameTemplate



from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerConfig(CustomConfig)
