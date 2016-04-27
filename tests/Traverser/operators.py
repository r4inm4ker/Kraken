from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.core.objects.operators.kl_operator import KLOperator
from kraken.core.traverser.traverser import Traverser

locInA = Locator("locatorInA")
locInB = Locator("locatorInB")
locOutA = Locator("locatorOutA")
locOutB = Locator("locatorOutB")

operator = KLOperator("IK", "MultiPoseConstraintSolver", "Kraken")
operator.resizeInput('constrainers', 2)
operator.resizeOutput('constrainees', 2)
operator.setInput("constrainers", locInA, 0)
operator.setInput("constrainers", locInB, 1)
operator.setOutput("constrainees", locOutA, 0)
operator.setOutput("constrainees", locOutB, 1)

trav = Traverser()
trav.addRootItem(locOutA)
trav.addRootItem(locOutB)

def callback(**args):
    item = args.get('item', None)
    print 'Visited '+item.getDecoratedPath()

trav.traverse(itemCallback = callback)
