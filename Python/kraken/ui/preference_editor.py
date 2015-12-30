
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

import os
import json

from PySide import QtGui, QtCore


class PreferenceEditor(QtGui.QDialog):
    """A widget providing the ability to nest """

    def __init__(self, parent=None):

        # constructors of base classes
        super(PreferenceEditor, self).__init__(parent)
        self.setObjectName('PreferenceEditor')

        self.setWindowTitle('Preference Editor')
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.resize(600, 300)

        self.prefValueWidgets = []

        self.createLayout()
        self.createConnections()

    def createLayout(self):

        # Parent Layout
        self._topLayout = QtGui.QVBoxLayout()
        self._topLayout.setContentsMargins(0, 0, 0, 0)
        self._topLayout.setSpacing(0)

        self._mainWidget = QtGui.QWidget()
        self._mainWidget.setObjectName('mainPrefWidget')

        # Main Layout
        self._mainLayout = QtGui.QVBoxLayout(self._mainWidget)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

        self._preferenceLayout = QtGui.QGridLayout()
        self._preferenceLayout.setContentsMargins(10, 10, 10, 10)
        self._preferenceLayout.setSpacing(3)
        self._preferenceLayout.setColumnMinimumWidth(0, 200)
        self._preferenceLayout.setColumnStretch(0, 1)
        self._preferenceLayout.setColumnStretch(1, 2)

        # Add widgets based on type here
        preferences = self.parentWidget().window().preferences.getPreferences()
        i = 0
        for k, v in preferences.iteritems():
            labelFrameWidget = QtGui.QFrame()
            labelFrameWidget.setObjectName('prefLabelWidgetFrame')
            labelFrameWidget.setFrameStyle(QtGui.QFrame.NoFrame | QtGui.QFrame.Plain)
            labelFrameWidget.setToolTip(v['description'])
            labelFrameLayout = QtGui.QHBoxLayout()

            prefLabel = QtGui.QLabel(v['nice_name'], self)
            prefLabel.setProperty('labelClass', 'preferenceLabel')
            prefLabel.setObjectName(k + "_label")
            prefLabel.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
            prefLabel.setMinimumWidth(200)

            labelFrameLayout.addWidget(prefLabel)
            labelFrameWidget.setLayout(labelFrameLayout)

            self._preferenceLayout.addWidget(labelFrameWidget, i, 0)

            if v['type'] == 'bool':
                valueFrameWidget = QtGui.QFrame()
                valueFrameWidget.setObjectName('prefValueWidgetFrame')
                valueFrameWidget.setFrameStyle(QtGui.QFrame.NoFrame | QtGui.QFrame.Plain)
                valueFrameLayout = QtGui.QHBoxLayout()

                valueWidget = QtGui.QCheckBox(self)
                valueWidget.setObjectName(k + "_valueWidget")
                valueWidget.setChecked(v['value'])

                valueFrameLayout.addWidget(valueWidget)
                valueFrameWidget.setLayout(valueFrameLayout)

            self._preferenceLayout.addWidget(valueFrameWidget, i, 1, 1, 1)
            self.prefValueWidgets.append(valueWidget)

            i += 1

        # OK and Cancel buttons
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.setContentsMargins(10, 10, 10, 10)
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        buttonLayout.addWidget(buttons)

        # Menu Bar
        self.menu_bar = QtGui.QMenuBar()
        self.file_menu = self.menu_bar.addMenu('&File')
        self.importPrefAction = self.file_menu.addAction('&Import...')
        self.exportPrefAction = self.file_menu.addAction('&Export...')

        self._mainLayout.addWidget(self.menu_bar)
        self._mainLayout.addLayout(self._preferenceLayout)
        self._mainLayout.addStretch(1)
        self._mainLayout.addLayout(buttonLayout)

        self._topLayout.addWidget(self._mainWidget)
        self.setLayout(self._topLayout)

    def createConnections(self):
        self.importPrefAction.triggered.connect(self.importPrefs)
        self.exportPrefAction.triggered.connect(self.exportPrefs)


    def importPrefs(self):
        fileDialog = QtGui.QFileDialog(self)
        fileDialog.setOption(QtGui.QFileDialog.DontUseNativeDialog, on=True)
        fileDialog.setWindowTitle('Import Preferences')
        fileDialog.setDirectory(os.path.expanduser('~'))
        fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        fileDialog.setNameFilter('JSON files (*.json)')

        if fileDialog.exec_() == QtGui.QFileDialog.Accepted:
            filePath = fileDialog.selectedFiles()[0]

            with open(filePath, "r") as openPrefFile:
                loadedPrefs = json.load(openPrefFile)

                self.parentWidget().window().preferences.loadPreferences(loadedPrefs)
                self.updatePrefValues()

    def exportPrefs(self):

        fileDialog = QtGui.QFileDialog(self)
        fileDialog.setOption(QtGui.QFileDialog.DontUseNativeDialog, on=True)
        fileDialog.setWindowTitle('Export Preferences')
        fileDialog.setDirectory(os.path.expanduser('~'))
        fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        fileDialog.setNameFilter('JSON files (*.json)')
        fileDialog.setDefaultSuffix('json')

        if fileDialog.exec_() == QtGui.QFileDialog.Accepted:
            filePath = fileDialog.selectedFiles()[0]

            preferences = self.parentWidget().window().preferences.getPreferences()
            with open(filePath, "w+") as savePrefFile:
                json.dump(preferences, savePrefFile)


    def updatePrefValues(self):
        """Updates the preference widgets with the values from the preferences.

        This is used when loading preferences from a file so that the widgets in
        the UI match what was loaded.
        """

        preferences = self.parentWidget().window().preferences

        for widget in self.prefValueWidgets:
            prefName = widget.objectName().rsplit('_', 1)[0]
            pref = preferences.getPreference(prefName)
            if pref['type'] == 'bool':
                widget.setChecked(pref['value'])

    # =======
    # Events
    # =======
    def accept(self):

        preferences = self.parentWidget().window().preferences

        for widget in self.prefValueWidgets:
            if type(widget) == QtGui.QCheckBox:
                prefName = widget.objectName().rsplit('_', 1)[0]
                preferences.setPreference(prefName, widget.isChecked())

        super(PreferenceEditor, self).accept()

    def closeEvent(self, event):
        pass
