from libr.UtilLibrary.Event import Event


class ExitEvent(Event):
    def __init__(self):
        Event.__init__(self)