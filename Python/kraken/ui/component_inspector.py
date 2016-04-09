
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#


import sys
from PySide import QtGui, QtCore
from HAppkit_Editors import EditorFactory, GetterSetterController, BaseInspector
from kraken.core.kraken_system import KrakenSystem


class ComponentInspector(BaseInspector):

    def __init__(self, component, parent=None, nodeItem=None):

        # constructors of base classes
        super(ComponentInspector, self).__init__(objectname='componentInspector', parent=parent)

        self.component = component
        self.nodeItem = nodeItem

        self.setWindowTitle(self.component.getName() + ":" + self.component.getTypeName())
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(300, 300)

        self.refresh()


    def refresh(self, data=None):
        self.clear()

        def setName(value):
            # Store original node name
            origName = self.nodeItem.getName()
            self.component.setName(value)
            if origName != self.component.getDecoratedName():
                self.nodeItem.setName(self.component.getDecoratedName())

        def getName():
            return self.component.getName()

        nameController = GetterSetterController('name', 'String', getter=getName, setter=setName)
        self.nameWidget = EditorFactory.constructEditor(nameController, parent=self)
        self.addEditor("name", self.nameWidget)

        def setLocation(value):
            # Store original node name
            origName = self.nodeItem.getName()
            self.component.setLocation(value)
            if origName != self.component.getDecoratedName():
                self.nodeItem.setName(self.component.getDecoratedName())

                # this is a hack to force the UI to update to reflect changes in the rig.
                # Ideally, we should be using an MVC pattern where the UI listens to changes
                # in the model, but we don't have an event system in KRaken. Instead we have to
                # push changes to the UI widgets. (an awkward and not-scalable solution.)
                # self.nameWidget.setWidgetValue(self.component.getName())

        def getLocation():
            return self.component.getLocation()

        locationController = GetterSetterController('location', 'String', getter=getLocation, setter=setLocation)
        locationWidget = EditorFactory.constructEditor(locationController, parent=self)
        self.addEditor("location", locationWidget)

        def displayAttribute(attribute):

            def setValue(value):
                attribute.setValue(value)

            def getValue():
                return attribute.getValue()

            attributeController = GetterSetterController(attribute.getName(), attribute.getDataType(), getter=getValue, setter=setValue)
            if attribute.getDataType() in ('Integer', 'Scalar'):
                attributeController.setOption('range', {'min': attribute.getMin(), 'max': attribute.getMax()})

            attributeWidget = EditorFactory.constructEditor(attributeController, parent=self)
            self.addEditor(attribute.getName(), attributeWidget)

        for i in xrange(self.component.getNumAttributeGroups()):
            attrGrp = self.component.getAttributeGroupByIndex(i)
            if attrGrp.getName() == "implicitAttrGrp":
                continue

            grp = self.component.getAttributeGroupByIndex(i)
            self.addSeparator(grp.getName())
            for j in xrange(grp.getNumAttributes()):
                displayAttribute(grp.getAttributeByIndex(j))

        # Add a stretch so that the widgets pack at the top.
        self.addStretch(2)

    # =======
    # Events
    # =======
    def closeEvent(self, event):
        if self.nodeItem is not None:
            self.nodeItem.inspectorClosed()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    from kraken_components.biped.arm_component import ArmComponentGuide
    armGuide = ArmComponentGuide("arm")

    widget = ComponentInspector(component=armGuide)
    widget.show()
    sys.exit(app.exec_())
