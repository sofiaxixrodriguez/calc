from libr.UtilLibrary.Event import Event

class ModeSwitchEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.__mode = None

    def setMode(self, mode):
        self.__mode = mode

    def getMode(self):
        return self.__mode
