from abc import ABCMeta, abstractmethod

class AbstractModel(metaclass=ABCMeta):
    @abstractmethod
    def parseData(self):
        pass