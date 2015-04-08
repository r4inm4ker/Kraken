from kraken import plugins
from kraken.core.objects.locator import Locator


myLoc = Locator("myLocator")

builder = plugins.getBuilder()
config = builder.getConfig()
config.setExplicitNaming(True)
builder.build(myLoc)

logHierarchy(myLoc)