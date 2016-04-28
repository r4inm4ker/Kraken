from kraken import plugins
from kraken.core.maths import Vec3
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.locator import Locator
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.traverser.traverser import Traverser
from kraken_examples.mainSrt_component import MainSrtComponentRig

mainComponent = MainSrtComponentRig('main')

trav = Traverser()
trav.addRootItem(mainComponent)

items = trav.traverse(discoverCallback = trav.discoverChildren)

trav.reset()
trav.addRootItems(items)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getPath()

trav.traverse(itemCallback = callback)

