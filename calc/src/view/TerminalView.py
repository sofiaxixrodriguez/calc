import sys

from libr.UtilLibrary.Subscriber import Subscriber
from libr.UtilLibrary.Publisher import Publisher

from src.Init import Modes, Operations, EventType


class TerminalView(Subscriber, Publisher):

    def __init__(self):
        Subscriber.__init__(self)
        Publisher.__init__(self)

        self.__text = ""
        self.__step = EventType.MODE
        self.__operandsNeeded = 1
        self.__currentMode = Modes.BASE          # ← was None
        self.__awaitingSeed = False
        self.__lastResult = 0.0

    # ==================================================
    # DISPLAY
    # ==================================================

    def setText(self, text, step, operandsNeeded=1, currentMode=None):
        self.__text = text
        self.__step = step

        if step == EventType.DATA and isinstance(operandsNeeded, int):
            self.__operandsNeeded = operandsNeeded
        elif step == EventType.RESULT and isinstance(operandsNeeded, (int, float)):
            self.__lastResult = float(operandsNeeded)

        if currentMode is not None:
            self.__currentMode = currentMode

        self.showScreen()

    def showScreen(self):
        print(self.__text)
        match self.__step:
            case EventType.MODE:      self.__requestMode()
            case EventType.OPERATION: self.__requestOperation()
            case EventType.DATA:      self.__requestData()
            case EventType.RESULT:    self.__requestContinue()

    # ==================================================
    # INITIAL PROMPT (seed / mode / exit)  — OOP's starter_num
    # ==================================================

    def __requestMode(self):
        userInput = input("> ").strip().lower()

        if userInput == Operations.EXIT.value:
            print(f"Resultado final: {self.__lastResult}")
            sys.exit()

        mode = self.__strToMode(userInput)
        if mode is not None:
            self.__currentMode = mode
            self.__awaitingSeed = True
            self.eventMap["ModeSwitchEvent"].setMode(mode)
            self.dispatchEvent(self.eventMap["ModeSwitchEvent"])
            return

        try:
            seed = float(userInput)
        except ValueError:
            print("No es un número válido ni un modo. Intenta de nuevo.")
            self.showScreen()
            return

        self.__lastResult = seed
        self.__awaitingSeed = False
        self.eventMap["SeedEvent"].setValue(seed)
        self.dispatchEvent(self.eventMap["SeedEvent"])

    # ==================================================
    # OPERATION PROMPT (also handles late mode switches / seed)
    # ==================================================

    def __requestOperation(self):
        userInput = input("> ").strip().lower()

        if userInput == Operations.EXIT.value:
            print(f"Resultado final: {self.__lastResult}")
            sys.exit()

        mode = self.__strToMode(userInput)
        if mode is not None:
            self.__currentMode = mode
            self.eventMap["ModeSwitchEvent"].setMode(mode)
            self.dispatchEvent(self.eventMap["ModeSwitchEvent"])
            return

        if self.__awaitingSeed:
            try:
                seed = float(userInput)
                self.__lastResult = seed
                self.__awaitingSeed = False
                self.eventMap["SeedEvent"].setValue(seed)
                self.dispatchEvent(self.eventMap["SeedEvent"])
                return
            except ValueError:
                pass

        operation = self.__strToOperation(userInput)
        if operation is None:
            print("Operación no reconocida. Intenta de nuevo.")
            self.showScreen()
            return

        self.__awaitingSeed = False
        self.eventMap["ExecuteOperationEvent"].setOperation(operation)
        self.dispatchEvent(self.eventMap["ExecuteOperationEvent"])

    # ==================================================
    # DATA COLLECTION
    # ==================================================

    def __requestData(self):
        operands = []
        for _ in range(self.__operandsNeeded):
            userInput = input("> ").strip()
            if userInput.lower() == Operations.EXIT.value:
                print(f"Resultado final: {self.__lastResult}")
                sys.exit()
            operands.append(userInput)

        self.eventMap["RecieveDataEvent"].setData(operands)
        self.dispatchEvent(self.eventMap["RecieveDataEvent"])

    # ==================================================
    # RESULT SCREEN
    # ==================================================

    def __requestContinue(self):
        # Match OOP: immediately continue to the next operation prompt.
        # The [Resultado actual: X] line was already printed by the RESULT event.
        self.__requestOperation()

    # ==================================================
    # PARSERS
    # ==================================================

    def __strToMode(self, mode):
        match mode:
            case Modes.BASE.value:        return Modes.BASE
            case Modes.SCIENTIFIC.value:  return Modes.SCIENTIFIC
            case Modes.PROGRAMMING.value: return Modes.PROGRAMMING
            case _:                       return None

    def __strToOperation(self, operation):
        match operation:
            case Operations.ADD.value:            return Operations.ADD
            case Operations.SUBTRACT.value:       return Operations.SUBTRACT
            case Operations.MULTIPLY.value:       return Operations.MULTIPLY
            case Operations.DIVIDE.value:         return Operations.DIVIDE
            case Operations.POWER.value:          return Operations.POWER
            case Operations.FACTORIAL.value:      return Operations.FACTORIAL
            case Operations.SQUARE_ROOT.value:    return Operations.SQUARE_ROOT
            case Operations.SECOND_DEGREE.value:  return Operations.SECOND_DEGREE
            case Operations.DECIMAL_TO_HEX.value: return Operations.DECIMAL_TO_HEX
            case _:                               return None