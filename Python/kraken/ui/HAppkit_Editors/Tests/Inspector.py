
#
# Copyright 2015 Fabric Technologies Inc. All rights reserved.
#

import os
import sys
import imp

from PySide import QtGui, QtCore

moduleDir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
sys.path.append(os.path.normpath(os.path.join(moduleDir, '..')))

from HAppkit_Editors.fe import FE
from HAppkit_Editors.base_inspector import BaseInspector
from HAppkit_Editors.core.pyval_controller import PyValController
from HAppkit_Editors.core.rtval_controller import RTValController
from HAppkit_Editors.core.undo_redo_manager import UndoRedoManager

app = QtGui.QApplication(sys.argv)
widget = BaseInspector()

# load the css
widget.setStyleSheet(open(os.path.join(moduleDir, 'editor_widgets.css')).read())


def undo():
    print "undo"
    UndoRedoManager.getInstance().logDebug()
    UndoRedoManager.getInstance().undo()

def redo():
    print "redo"
    UndoRedoManager.getInstance().logDebug()
    UndoRedoManager.getInstance().redo()

undoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z), widget)
undoShortcut.setContext(QtCore.Qt.ApplicationShortcut)
undoShortcut.activated.connect(undo)

redoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Y), widget)
undoShortcut.setContext(QtCore.Qt.ApplicationShortcut)
redoShortcut.activated.connect(redo)


fetypes = FE.getInstance().types()

widget.addControllerEditor( PyValController('myString', 'String', 'Hello') )
widget.addControllerEditor( PyValController('myMultilineString', 'String', 'Hello\nWorld\nYou\nGuys', multiLine={ 'numLines':6 } ) )
widget.addControllerEditor( PyValController('myStringArray', 'String[]', []) )
widget.addControllerEditor( PyValController('myStringDict', 'String[String]', {}) )
widget.addControllerEditor( PyValController('myInteger', 'Integer', 32) )
widget.addControllerEditor( PyValController('myScalar', 'Scalar', 3.2) )

widget.addControllerEditor( PyValController('myIntegerRange', 'Integer', 32, range = {'min': 10, 'max': 50 }) )
widget.addControllerEditor( PyValController('myScalarRange', 'Scalar', 3.2, range = {'min': 1.0, 'max': 5.0 }) )

widget.addControllerEditor( PyValController('myIntegerList', 'Integer', 1, combo = ['Option1', 'Option2', 'Option3' ] ) )
widget.addControllerEditor( PyValController('myStringList', 'String', 1, combo = ['Option1', 'Option2', 'Option3' ] ) )

widget.addControllerEditor( PyValController('vec2', 'Vec2', value=fetypes.Vec2() ) )
widget.addControllerEditor( PyValController('vec3', 'Vec3', value=fetypes.Vec3() ) )
widget.addControllerEditor( PyValController('vec4', 'Vec4', value=fetypes.Vec4() ) )
widget.addControllerEditor( RTValController('xfo', 'Xfo', value=fetypes.Xfo() ) )

widget.addControllerEditor( RTValController('color', 'Color', value=fetypes.Color() ) )

widget.addControllerEditor( RTValController('fileSave', 'FilePath', value=fetypes.FilePath.create(os.path.realpath(__file__)), WriteFile={
    'Title': 'Choose file to write...',
    'Filter': '"Python Files(*.py)'
    } ) )

widget.addControllerEditor( RTValController('fileLoad', 'FilePath', value=fetypes.FilePath.create("C:/Foo.txt"), ReadFile={
    'Title': 'Choose file to Load...',
    'Filter': '"Text Files(*.txt)'
    } ) )

widget.addStretch(1)

UndoRedoManager.getInstance().enable()
widget.show()
sys.exit(app.exec_())

