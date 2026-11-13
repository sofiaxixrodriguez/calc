from libr.UtilLibrary.Event import Event


class SeedEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.__value = None

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value