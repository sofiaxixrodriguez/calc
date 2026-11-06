from libr.UtilLibrary.Event import Event

class ExecuteOperationEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.__operation = None

    def setOperation(self, operation):
        self.__operation = operation

    def getOperation(self):
        return self.__operation