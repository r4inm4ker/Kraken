
import os
import sys
import __builtin__
import importlib
import traceback

class ModuleImportManager:
    def __init__(self):
        "Creates an instance and installs as the global importer"
        self.previousModules = sys.modules.copy()
        self.realImport = __builtin__.__import__
        __builtin__.__import__ = self._import
        self.newModules = {}
        self.protectedModules = ['os', 'kraken.core', 'kraken.helpers', 'kraken.plugins', 'kraken.ui', 'FabricEngine', 'pyflowgraph', 'GraphView']

    def _import(self, name, globals=None, locals=None, fromlist=[]):
        result = apply(self.realImport, (name, globals, locals, fromlist))
        if len(name.split('.')) == 1:
            return result
        for p in self.protectedModules:
            if name.startswith(p):
                return result
        self.newModules[name] = 1
        # print '_import:' + name #+ ' globals:' + str(globals) + ' locals:' + str(locals) + ' fromlist:' + str(fromlist)
        return result

    def uninstall(self):
        for modname in self.newModules.keys():
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                if modname in sys.modules:
                    del(sys.modules[modname])
        __builtin__.__import__ = self.realImport

    def reload(self):
        reloadedModules = self.newModules.copy()

        for modname in self.newModules.keys():
            if not self.previousModules.has_key(modname):
                # Force reload when modname next imported
                if modname in sys.modules:
                    del(sys.modules[modname])

        self.newModules = {}

        for modname in reloadedModules:
            try:
                importlib.import_module(modname)
            except Exception as e:
                stack = traceback.format_tb(sys.exc_info()[2])
                exception_list = []
                exception_list.extend(stack)
                exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

                exception_str = "Traceback (most recent call last):\n"
                exception_str += "".join(exception_list)
                # Removing the last \n
                exception_str = exception_str[:-1]
                print(exception_str)
