

import json, difflib
import os.path
from PySide import QtGui, QtCore

from contextual_node_list import ContextualNodeList, ContextualNewNodeWidget
from graph_view import GraphView

from kraken.core.objects.rig import Rig
from kraken import plugins


def GetHomePath():
    from os.path import expanduser
    homeDir = expanduser("~")
    return homeDir

class GraphViewWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)

        self.graphView = GraphView(parent=self)
        self.__contextualNodeList = None

        # setup the toobar
        toolBar = QtGui.QToolBar()

        newAction = toolBar.addAction('New')
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.newRigPreset)
        newAction.setObjectName("newButton")

        saveAction = toolBar.addAction('Save')
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveRigPreset)
        saveAction.setObjectName("saveButton")

        loadAction = toolBar.addAction('Load')
        loadAction.setShortcut('Ctrl+S')
        loadAction.triggered.connect(self.loadRigPreset)
        saveAction.setObjectName("loadButton")

        toolBar.addSeparator()

        # Setup the name widget
        toolBar.addWidget(QtGui.QLabel('Name:'))
        self.nameWidget = QtGui.QLineEdit('', self)
        def setRigName( text ):
            self.guideRig.setName( text )
        self.nameWidget.textChanged.connect(setRigName)
        toolBar.addWidget( self.nameWidget )

        toolBar.addSeparator()

        buildGuideAction = toolBar.addAction('Build Guide')
        buildGuideAction.triggered.connect(self.buildGuideRig)

        # synchGuideAction = toolBar.addAction('Synch Guide')
        # synchGuideAction.triggered.connect(self.synchGuideRig)

        buildGuideAction = toolBar.addAction('Build Rig')
        buildGuideAction.triggered.connect(self.buildRig)

        #########################
        ## Setup hotkeys for the following actions.

        deleteShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(toolBar)
        layout.addWidget(self.graphView)

        self.setLayout(layout)

        self.newRigPreset()

    def newRigPreset(self):
        # TODO: clean the rig from the scene if it has been built.
        self.guideRig = Rig()
        self.graphView.init( self.guideRig )
        self.nameWidget.setText( 'MyRig' )

    def saveRigPreset(self):
        lastSceneFilePath = os.path.join(GetHomePath(), self.guideRig.getName() )
        (filePath, filter) = QtGui.QFileDialog.getSaveFileName(self, 'Save Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.synchGuideRig()
            self.guideRig.writeRigDefinitionFile(filePath)

    def loadRigPreset(self):
        lastSceneFilePath = GetHomePath()
        (filePath, filter) = QtGui.QFileDialog.getOpenFileName(self, 'Load Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.guideRig = Rig()
            self.guideRig.loadRigDefinitionFile(filePath)
            self.graphView.init( self.guideRig )
            self.nameWidget.setText( self.guideRig.getName() )

    def buildGuideRig(self):
        builder = plugins.getBuilder()

        if self.guideRig.getName().endswith('_guide') is False:
            self.guideRig.setName(self.guideRig.getName() + '_guide')

        builder.build(self.guideRig)

    def synchGuideRig(self):
        synchronizer = plugins.getSynchronizer()
        synchronizer.setTarget(self.guideRig)
        synchronizer.sync()

    def buildRig(self):
        self.synchGuideRig()

        rigBuildData = self.guideRig.getRigBuildData()
        rig = Rig()
        rig.loadRigDefinition(rigBuildData)

        rig.setName(rig.getName().replace('_guide', ''))

        builder = plugins.getBuilder()
        builder.build(rig)

    def keyPressEvent(self, event):
        if event.key() == 96: #'`'
            pos = self.mapFromGlobal(QtGui.QCursor.pos());
            if not self.__contextualNodeList:
                self.__contextualNodeList = ContextualNodeList(self)


            scenepos = self.graphView.getGraph().mapToScene(pos)

            # xfo = self.graphView.getGraph().itemGroup().transform()
            # scenepos = xfo.map(pos)
            # print "pos:" + str(pos)
            # print "scenepos:" + str(scenepos)
            self.__contextualNodeList.showAtPos(pos, scenepos)

