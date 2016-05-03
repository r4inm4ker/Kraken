import logging


class WidgetHandler(logging.Handler):
    """Logging Handler for Sending Messages to Widgets."""

    def __init__(self):
        super(WidgetHandler, self).__init__()
        self._widgets = []

    def addWidget(self, widget):
        if widget not in self._widgets:
            self._widgets.append(widget)

    def removeWidget(self, widget):
        if widget in self._widgets:
            self._widgets.remove(widget)

    def clearWidgets(self):
        self._widgets = []

    def emit(self, record):

        msg = self.format(record)

        for widget in self._widgets:
            widget.write(msg + '\n', record.levelname)
