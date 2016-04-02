
from kraken.core.objects.components.component import Component

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.hierarchy_group import HierarchyGroup


class BaseExampleComponent(Component):
    """Example Component Base"""

    def __init__(self, name='', parent=None, data=None):
        super(BaseExampleComponent, self).__init__(name, parent)

        # ================
        # Setup Hierarchy
        # ================
        self.controlsLayer = self.getOrCreateLayer('controls')
        self.ctrlCmpGrp = ComponentGroup(self.getName(), self, parent=self.controlsLayer)
        self.addItem('ctrlCmpGrp', self.ctrlCmpGrp)

        # IO Hierarchies
        self.inputHrcGrp = HierarchyGroup('inputs', parent=self.ctrlCmpGrp)
        self.cmpInputAttrGrp = AttributeGroup('inputs', parent=self.inputHrcGrp)

        self.outputHrcGrp = HierarchyGroup('outputs', parent=self.ctrlCmpGrp)
        self.cmpOutputAttrGrp = AttributeGroup('outputs', parent=self.outputHrcGrp)


    def detach(self):
        """Detaches component from container. This method undoes the actions
        performed in the constructor. It removes all elements that were added
        to the rig. It is invoked by the UI when deleting components from a
        guide rig.
        """

        self.controlsLayer.removeChild(self.ctrlCmpGrp)
        container = self.getContainer()

        if self.controlsLayer.getNumChildren() == 0:
            container.removeChild(self.controlsLayer)
        container.removeChild(self)


    def attach(self, container):
        """Attaches component to container.

        Args:
            container (object): container to attach to.

        """

        if not container.hasChild(self.controlsLayer):
            container.addChild(self.controlsLayer)

        self.controlsLayer.addChild(self.ctrlCmpGrp)
        container.addChild(self)


