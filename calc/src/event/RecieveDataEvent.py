from libr.UtilLibrary.Event import Event

class RecieveDataEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.__data = None

    def setData(self, data):
        self.__data = data

    def getData(self):
        return self.__data