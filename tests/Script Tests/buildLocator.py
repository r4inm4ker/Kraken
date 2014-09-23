from kraken import plugins
from kraken.core.objects.locator import Locator

myLoc = Locator("myLocator")

builder = plugins.getBuilder()
builder.build(myLoc)