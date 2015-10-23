

#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

import os
import sys


krakenDir = os.path.dirname(os.path.realpath(__file__))
# krakenDir=os.path.abspath(os.path.join(krakenModuleDir, '..', '..'))


os.environ['KRAKEN_PATH']  = krakenDir

fabricEngineDir=os.path.normpath("D:/temp/FabricEngine-2.0.0-Windows-x86_64/")
# fabricEngineDir=os.path.normpath("D:/temp/FabricEngine-1.15.2-Windows-x86_64/")

os.environ['PATH'] = os.path.join(fabricEngineDir, 'bin') + ';' + os.environ['PATH']

PYTHON_VERSION = sys.version[:3]
sys.path.append( os.path.join(fabricEngineDir, 'Python', PYTHON_VERSION ) )

os.environ['FABRIC_EXTS_PATH'] = os.path.join(fabricEngineDir, 'Exts') + ';' + os.path.join(krakenDir, 'KLExts') + ';' + os.environ['FABRIC_EXTS_PATH']

os.environ['KRAKEN_PATHS'] = os.path.join(krakenDir, 'extraComponents')

from PySide import QtGui
from kraken.ui.kraken_window import KrakenWindow, createSplash

app = QtGui.QApplication(sys.argv)

splash = createSplash(app)

window = KrakenWindow()
window.show()

splash.finish(window)

sys.exit(app.exec_())
