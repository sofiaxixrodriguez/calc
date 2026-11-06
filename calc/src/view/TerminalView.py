import sys

from libr.UtilLibrary.Subscriber import Subscriber
from libr.UtilLibrary.Publisher import Publisher

from src.Init import (
    Modes,
    Operations,
    EventType
)


class TerminalView(Subscriber, Publisher):

    def __init__(self):

        Subscriber.__init__(self)
        Publisher.__init__(self)

        self.__text = ""

        self.__step = EventType.MODE

        self.__operandsNeeded = 1

        self.__currentMode = None

    # ==================================================
    # DISPLAY
    # ==================================================

    def setText(
            self,
            text,
            step,
            operandsNeeded=1,
            currentMode=None
    ):

        self.__text = text
        self.__step = step
        self.__operandsNeeded = operandsNeeded

        if currentMode is not None:
            self.__currentMode = currentMode

        self.showScreen()

    # ==================================================
    # SCREEN ROUTER
    # ==================================================

    def showScreen(self):

        print(self.__text)

        match self.__step:

            case EventType.MODE:
                self.__requestMode()

            case EventType.OPERATION:
                self.__requestOperation()

            case EventType.DATA:
                self.__requestData()

            case EventType.RESULT:
                self.__requestContinue()

    # ==================================================
    # MODE SELECTION
    # ==================================================

    def __requestMode(self):

        userInput = input().strip().lower()

        if userInput == Operations.EXIT.value:
            sys.exit()

        mode = self.__strToMode(userInput)

        if mode is None:
            self.showScreen()
            return

        self.__currentMode = mode

        self.eventMap["ModeSwitchEvent"].setMode(
            mode
        )

        self.dispatchEvent(
            self.eventMap["ModeSwitchEvent"]
        )

    # ==================================================
    # OPERATION SELECTION
    # ==================================================

    def __requestOperation(self):

        userInput = input().strip().lower()

        if userInput == Operations.EXIT.value:
            sys.exit()

        operation = self.__strToOperation(
            userInput
        )

        if operation is None:
            self.showScreen()
            return

        self.eventMap["ExecuteOperationEvent"].setOperation(
            operation
        )

        self.dispatchEvent(
            self.eventMap["ExecuteOperationEvent"]
        )

    # ==================================================
    # DATA COLLECTION
    # ==================================================

    def __requestData(self):

        operands = []

        for _ in range(self.__operandsNeeded):

            operands.append(
                input().strip()
            )

        self.eventMap["RecieveDataEvent"].setData(
            operands
        )

        self.dispatchEvent(
            self.eventMap["RecieveDataEvent"]
        )

    # ==================================================
    # RESULT SCREEN
    # ==================================================

    def __requestContinue(self):

        input(
            "\nPresiona ENTER para continuar..."
        )

        if self.__currentMode is not None:

            self.eventMap["ModeSwitchEvent"].setMode(
                self.__currentMode
            )

            self.dispatchEvent(
                self.eventMap["ModeSwitchEvent"]
            )

    # ==================================================
    # PARSERS
    # ==================================================

    def __strToMode(self, mode):

        match mode:

            case Modes.BASE.value:
                return Modes.BASE

            case Modes.SCIENTIFIC.value:
                return Modes.SCIENTIFIC

            case Modes.PROGRAMMING.value:
                return Modes.PROGRAMMING

            case _:
                return None

    def __strToOperation(self, operation):

        match operation:

            case Operations.ADD.value:
                return Operations.ADD

            case Operations.SUBTRACT.value:
                return Operations.SUBTRACT

            case Operations.MULTIPLY.value:
                return Operations.MULTIPLY

            case Operations.DIVIDE.value:
                return Operations.DIVIDE

            case Operations.POWER.value:
                return Operations.POWER

            case Operations.FACTORIAL.value:
                return Operations.FACTORIAL

            case Operations.SQUARE_ROOT.value:
                return Operations.SQUARE_ROOT

            case Operations.SECOND_DEGREE.value:
                return Operations.SECOND_DEGREE

            case Operations.DECIMAL_TO_HEX.value:
                return Operations.DECIMAL_TO_HEX

            case _:
                return None