

import FabricEngine.Core

class FE(object):
    __instance = None
    def __init__(self, client=None):
        super(FE, self).__init__()

        if client is not None:
            self.setClient(client)
        else:
            self.createClient()


    def createClient(self):
        def emitMessage(arg0, arg1=None, msg=None):
            print arg0
        self.setClient(FabricEngine.Core.createClient( { 'reportCallback': emitMessage, 'guarded': True } ))
        self.__feclient.loadExtension('Util')
        self.__feclient.loadExtension('FileIO')

    def setClient(self, client):
        self.__feclient = client
        self.__feclient.loadExtension('Math')
        self.__fetypes = client.RT.types
        self.__fetypeDescs = client.RT.getRegisteredTypes()

    def types(self):
        return self.__fetypes

    def rtVal(self, dataType, *args):
        klType = getattr(self.__fetypes, dataType)
        try:
            return apply(klType.create, *args)
        except:
            return klType(*args)

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = FE()
        return cls.__instance


    @classmethod
    def setInstance(cls, client):
        if cls.__instance is None:
            cls.__instance = FE(client)
        else:
            cls.__instance.setInstance(client)
