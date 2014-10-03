from kraken import plugins
from kraken.core.objects.locator import Locator

builder = plugins.getBuilder()

config = builder.getConfig()
config.setExplicitNaming(True)

myLoc = Locator("myLocator")
builder.build(myLoc)