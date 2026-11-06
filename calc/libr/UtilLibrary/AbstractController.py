from abc import ABCMeta, abstractmethod


class AbstractController(metaclass=ABCMeta):
    @abstractmethod
    def setAsociatedViews(self, *args):
        pass

    @abstractmethod
    def setAsociatedModels(self, *args):
        pass