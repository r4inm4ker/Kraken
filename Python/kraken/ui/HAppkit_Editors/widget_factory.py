

class EditorFactory(object):

    __registeredEditors = []

    def __init__(self):
        super(EditorFactory, self).__init__()

    @classmethod
    def registerEditorClass(cls, widgetClass):
        cls.__registeredEditors.append(widgetClass)

    @classmethod
    def constructEditor(cls, valueController, parent=None):

        for widgetCls in reversed(cls.__registeredEditors):
            if widgetCls.canDisplay(valueController):
                return widgetCls(valueController, parent=parent)

        raise Exception("No Editors registered for the given controller:" + valueController.getName() + ":" + valueController.getDataType())

