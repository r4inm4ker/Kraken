from kraken import plugins
from kraken.core.maths import Vec3
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.locator import Locator
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.traverser.traverser import Traverser
from kraken_examples.spine_component import SpineComponentRig
from kraken_examples.clavicle_component import ClavicleComponentRig

spineComponent = SpineComponentRig('spine')
spineComponent.loadData(data={
    'cogPosition': Vec3(0.0, 11.1351, -0.1382),
    'spine01Position': Vec3(0.0, 11.1351, -0.1382),
    'spine02Position': Vec3(0.0, 11.8013, -0.1995),
    'spine03Position': Vec3(0.0, 12.4496, -0.3649),
    'spine04Position': Vec3(0.0, 13.1051, -0.4821),
    'numDeformers': 4
})
clavComponent = ClavicleComponentRig('clavicle')

vertebraeOutputs = spineComponent.getOutputByName('spineVertebrae')
clavicleSpineEndInput = clavComponent.getInputByName('spineEnd')
clavicleSpineEndInput.setConnection(vertebraeOutputs, 2)

trav = Traverser()
trav.addRootItem(spineComponent)
trav.addRootItem(clavComponent)

items = trav.traverse(discoverCallback = trav.discoverChildren)

trav.reset()
trav.addRootItems(items)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getDecoratedPath()

trav.traverse(itemCallback = callback)
