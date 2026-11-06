from abc import ABC, abstractmethod


class LinkElementsInterface(ABC):
    @abstractmethod
    def linkControllers(self):
        pass

    @abstractmethod
    def linkViews(self):
        pass

    @abstractmethod
    def linkModels(self):
        pass

    @abstractmethod
    def registerEvents(self):
        pass
