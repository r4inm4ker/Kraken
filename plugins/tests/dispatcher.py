from kraken.core.objects import elements

from kraken.kraken_si.utils import *
from kraken.plugins import si_plugin
reload(si_plugin)


myNull = elements.Null("myNull")
myNull.xfo.tr.y = 5
myNull.visibility = False

myNull2 = elements.Null("myNull2", parent=myNull)
myNull2.color = "red"
myNull3 = elements.Null("myNull3", parent=myNull2)

siDispatcher = si_plugin.Dispatcher(myNull)
siDispatcher.create()