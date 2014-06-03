from win32com.client import constants
from win32com.client.dynamic import Dispatch
from kraken.core.objects import elements

si = Application
log = si.LogMessage
sel = si.Selection

DEBUG = 0


inst = elements.Null
        
def _siBuild(self):
    
    self.object3D = self.parent.object3D.AddNull()
        
        
def _siSetObjName(self):
    """Sets object3D name.

    Return:
    True if successful.

    """

    self.object3D.Name = self.buildName()

    return True


class Scene(object):
    """Softimage Scene Root."""

    def __init__(self, app="si"):
        super(Scene, self).__init__()
        self.app = app
        self.object3D = si.ActiveProject3.ActiveScene.Root


    def __str__(self):
        return str("Kraken Scene: " + self.object3D.Name)

        
def _siCheckParent(self):
        """Check if parent is set, if not set to scene root."""

        if self.parent is None:
            self.parent = Scene()

        return
        
    
inst._build = _siBuild
inst._setObjName = _siSetObjName
inst._checkParent = _siCheckParent


myNull = elements.Null("myNull")
myNull2 = elements.Null("myNull2", parent=myNull)


log(myNull.children)

myNull.build()