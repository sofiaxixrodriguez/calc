from libr.UtilLibrary.Event import Event


class KeepResultEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.__operation = None
        self.__value = None

    def setOperation(self, operation):
        self.__operation = operation

    def getOperation(self):
        return self.__operation

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value