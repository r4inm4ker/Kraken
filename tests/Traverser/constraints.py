from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.traverser.traverser import Traverser

locA = Locator("locatorA")
locB = Locator("locatorB")

constraint = PoseConstraint("A to B")
constraint.addConstrainer(locB)
constraint.setConstrainee(locA)

trav = Traverser()
trav.addRootItem(locA)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getDecoratedPath()

trav.traverse(itemCallback = callback)
