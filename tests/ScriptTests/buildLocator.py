from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.helpers.utility_methods import logHierarchy


myLoc = Locator("myLocator")

builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

builder.build(myLoc)

logHierarchy(myLoc)
