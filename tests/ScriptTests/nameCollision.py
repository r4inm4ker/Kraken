from kraken import plugins
from kraken.core.objects.locator import Locator
from kraken.helpers.utility_methods import logHierarchy


if __name__ == '__main__':

    try:
        myParent = Locator("myParent")
        myLoc1 = Locator("myLocator1", parent=myParent)
        myLoc2 = Locator("myLocator1", parent=myParent)

    except Exception as e:
        print e

    try:
        myParent = Locator("myParent")
        myLoc1 = Locator("myLocator1", parent=myParent)
        myLoc2 = Locator("myLocator2", parent=myParent)

        myLoc2.setName("myLocator1")

    except Exception as e:
        print e
