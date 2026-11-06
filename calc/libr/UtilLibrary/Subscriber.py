from abc import abstractmethod


class Subscriber():
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def onEventReceived(self, event):
        pass