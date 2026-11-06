from libr.UtilLibrary.Publisher import Publisher
from libr.UtilLibrary.AbstractModel import AbstractModel

from src.Init import Modes
from src.Init import EventType


class SelectModeModel(AbstractModel, Publisher):

    def __init__(self):
        AbstractModel.__init__(self)
        Publisher.__init__(self)

        self.parseData()

    def parseData(self):

        self.__currentMode = Modes.BASE

    # ==========================================
    # MODE
    # ==========================================

    def setMode(self, mode):

        self.__currentMode = mode

        self.eventMap["UpdateDataEvent"].setStep(
            EventType.OPERATION
        )

        self.eventMap["UpdateDataEvent"].setType(
            mode
        )

        self.eventMap["UpdateDataEvent"].setData(
            None
        )

        self.dispatchEvent(
            self.eventMap["UpdateDataEvent"]
        )

    def getMode(self):
        return self.__currentMode