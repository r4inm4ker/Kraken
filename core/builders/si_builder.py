
from kraken.core.objects.curve import Curve
from kraken.core.objects.component import BaseComponent
from kraken.core.objects.controls.base_control import BaseControl

from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from base_builder import BaseBuilder
from win32com.client import Dispatch

si = Dispatch("XSI.Application").Application
log = si.LogMessage


class SIBuilder(BaseBuilder):
    """Softimage Builder"""

    def __init__(self):
        super(SIBuilder, self).__init__()


    def buildAttributes(self, sceneItem, object3D):

        for i in xrange(sceneItem.getNumAttributes()):
            attribute = sceneItem.getAttributeByIndex(i)

            if isinstance(attribute, FloatAttribute):
                log(attribute.name)

            elif isinstance(attribute, BoolAttribute):
                log(attribute.name)

            elif isinstance(attribute, IntegerAttribute):
                log(attribute.name)

            elif isinstance(attribute, StringAttribute):
                log(attribute.name)

        return


    def buildHierarchy(self, sceneItem, parentObject3D, component=None):

        object3D = None

        if sceneItem.testFlag('guide'):
            return None

        # Build Object
        if isinstance(sceneItem, BaseComponent):
            object3D = parentObject3D.AddNull(self.buildName(sceneItem, component=None))
            component = sceneItem

        elif isinstance(sceneItem, Curve):
            object3D = parentObject3D.AddNull(self.buildName(sceneItem, component=component))

        elif isinstance(sceneItem, BaseControl):
            object3D = parentObject3D.AddNull(self.buildName(sceneItem, component=component))

        else:
            raise NotImplementedError(sceneItem.getName() + ' has an unsupported type: ' + str(type(sceneItem)))

        # Build Attributes
        if object3D is not None:
            self.buildAttributes(sceneItem, object3D)

        # Build children
        for i in xrange(sceneItem.getNumChildren()):
            child = sceneItem.getChildByIndex(i)
            self.buildHierarchy(child, object3D, component)

        return object3D


    def buildName(self, sceneItem, component=None):

        if isinstance(sceneItem, BaseComponent):
            return '_'.join([sceneItem.getName(), sceneItem.getSide(), 'hrc'])

        componentName = ""
        side = ""

        if component is not None:
            componentName = component.getName()
            side = component.getSide()

        elif isinstance(sceneItem, Curve):
            return '_'.join([componentName, sceneItem.getName(), side, 'crv'])

        elif isinstance(sceneItem, BaseControl):
            return '_'.join([componentName, sceneItem.getName(), side, 'ctrl'])
        else:
            raise NotImplementedError('buildName() not implemented for ' + str(type(sceneItem)))

        return None


    def build(self, container):
        """Builds the supplied container into a DCC representation.

        Arguments:
        container -- Container, kraken container object to build.

        Return:
        True if successful.
        """

        scnRoot = si.ActiveProject3.ActiveScene.Root

        containerNull = scnRoot.AddNull(container.name)

        armatureLayer = containerNull.AddNull(container.name + "_armature")
        controlLayer = containerNull.AddNull(container.name + "_controls")
        geometryLayer = containerNull.AddNull(container.name + "_geometry")

        # Create Each Component
        for eachComponent in container.getChildrenByType(BaseComponent):
            self.buildHierarchy(eachComponent, controlLayer)

        return True