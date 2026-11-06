class Publisher:
    def __init__(self):
        self.eventMap: dict = {}

    def __del__(self):
        pass

    def addEvent(self, *args):
        for event in args:
            self.eventMap[str(event.__class__.__name__)] = event

    def dispatchEvent(self, event):
        event.notifyAll()
