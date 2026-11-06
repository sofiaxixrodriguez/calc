from libr.UtilLibrary.Event import Event

class UpdateDataEvent(Event):
    def __init__(self):
        Event.__init__(self)

        self.__type = None
        self.__data = None
        self.__step = None

    def setType(self, dataType):
        self.__type = dataType

    def getType(self):
        return self.__type

    def setData(self, data):
        self.__data = data

    def getData(self):
        return self.__data

    def setStep(self, step):
        self.__step = step

    def getStep(self):
        return self.__step