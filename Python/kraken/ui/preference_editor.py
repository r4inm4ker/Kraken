
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

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

        # layout
        self._mainLayout = QtGui.QVBoxLayout()
        self._mainLayout.setContentsMargins(10, 10, 10, 10)

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
            prefLabel = QtGui.QLabel(v['nice_name'], self)
            prefLabel.setProperty('labelClass', 'preferenceLabel')
            prefLabel.setObjectName(k + "_label")
            prefLabel.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
            prefLabel.setMinimumWidth(200)
            self._preferenceLayout.addWidget(prefLabel, i, 0)

            if v['type'] == 'bool':
                valueWidget = QtGui.QCheckBox(self)
                valueWidget.setObjectName(k + "_valueWidget")
                valueWidget.setChecked(v['value'])

            self._preferenceLayout.addWidget(valueWidget, i, 1, 1, 1)
            self.prefValueWidgets.append(valueWidget)

            i += 1

        # OK and Cancel buttons
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self._mainLayout.addLayout(self._preferenceLayout)
        self._mainLayout.addStretch(1)
        self._mainLayout.addWidget(buttons)

        self.setLayout(self._mainLayout)

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
