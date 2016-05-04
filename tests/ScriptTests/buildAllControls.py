from kraken import plugins
from kraken.core.objects.transform import Transform
from kraken.core.objects.control import Control
from kraken.helpers.utility_methods import logHierarchy

# Build
builder = plugins.getBuilder()
config = builder.getConfig()
config.setExplicitNaming(True)

ctrlParent = Transform("controls")

ctrlShapes = config.getControlShapes()

i = 0
j = 0
for k, v in ctrlShapes.iteritems():
    ctrl = Control(k + '_shape', shape=k, parent=ctrlParent)

    ctrl.xfo.tr.x = i % 5 * 2
    ctrl.xfo.tr.z = j * 2

    if i % 5 == 4:
        j += 1

    i += 1


builder.build(ctrlParent)

logHierarchy(ctrlParent)
