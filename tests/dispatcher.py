from kraken.core.objects import elements

from kraken.kraken_si.utils import *
from kraken.plugins import si_plugin
reload(si_plugin)


myNull = elements.Null("myNull")
myNull2 = elements.Null("myNull2", parent=myNull)

siDispatcher = si_plugin.Dispatcher(myNull)
siDispatcher.build()