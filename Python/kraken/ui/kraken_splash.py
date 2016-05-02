import re
import sys

from PySide import QtGui, QtCore

from kraken.ui import images_rc
from kraken.log import getLogger

logger = getLogger('kraken')


class KrakenSplash(QtGui.QSplashScreen):

    messageFlag = QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft

    def __init__(self, app, *arg, **kwargs):

        splashPixmap = QtGui.QPixmap(':/images/KrakenUI_Splash.png')
        super(KrakenSplash, self).__init__(splashPixmap)

        for handler in logger.handlers:
            if type(handler).__name__ == 'WidgetHandler':
                handler.addWidget(self)

        self._msg = []
        self._app = app
        self.setMask(splashPixmap.mask())
        self.showMessage('Releasing the Kraken!', self.messageFlag, QtCore.Qt.white)
        self._app.processEvents()

    # def write(self, msg):
    #     filtered = filter(lambda x: not re.match(r'^$', x), msg)

    #     if filtered != "":
    #         if len(self._msg) == 1:
    #             del self._msg[0]

    #         self._msg.append(filtered)

    #         self.showMessage("\n".join(self._msg), self.messageFlag, QtCore.Qt.white)

    def write(self, msg, level):
        filtered = filter(lambda x: not re.match(r'^$', x), msg)

        if filtered != "":
            self.showMessage(msg.rstrip(), self.messageFlag, QtCore.Qt.white)
