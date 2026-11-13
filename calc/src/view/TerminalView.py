import sys

from libr.UtilLibrary.Subscriber import Subscriber
from libr.UtilLibrary.Publisher import Publisher

from src.Init import Modes, Operations, EventType, OutputType


class TerminalView(Subscriber, Publisher):

    def __init__(self):
        Subscriber.__init__(self)
        Publisher.__init__(self)

        self.__text = ""
        self.__step = EventType.MODE
        self.__eventType = None
        self.__operandsNeeded = 1
        self.__currentMode = Modes.BASE
        self.__awaitingSeed = False
        self.__lastResult = None

    # ==================================================
    # DISPLAY
    # ==================================================

    def setText(self, text, step, data=1, currentMode=None, eventType=None):
        self.__text = text
        self.__step = step
        self.__eventType = eventType

        if step == EventType.DATA and isinstance(data, int):
            self.__operandsNeeded = data
        elif step == EventType.RESULT:
            self.__lastResult = data

        if currentMode is not None:
            self.__currentMode = currentMode

        self.showScreen()

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
                if self.__eventType == OutputType.FINAL_RESULT:
                    sys.exit()
                elif self.__eventType == OutputType.SCIENTIFIC_RESULT:
                    self.__requestKeepScientific()
                elif self.__eventType == OutputType.SECOND_DEGREE_RESULT:
                    self.__requestKeepSecondDegree()
                else:
                    self.__requestContinue()

    # ==================================================
    # EXIT FLOW
    # ==================================================

    def __triggerExit(self):
        """Ask the model for its accumulator and display it, then exit."""
        self.dispatchEvent(self.eventMap["ExitEvent"])
        sys.exit()  # fallback if dispatch returns normally

    # ==================================================
    # INITIAL PROMPT (seed / mode / exit)
    # ==================================================

    def __requestMode(self):
        userInput = input("> ").strip().lower()

        if userInput == Operations.EXIT.value:
            self.__triggerExit()

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

        self.__awaitingSeed = False
        self.eventMap["SeedEvent"].setValue(seed)
        self.dispatchEvent(self.eventMap["SeedEvent"])

    # ==================================================
    # OPERATION PROMPT
    # ==================================================

    def __requestOperation(self):
        userInput = input("> ").strip().lower()

        if userInput == Operations.EXIT.value:
            self.__triggerExit()

        mode = self.__strToMode(userInput)
        if mode is not None:
            self.__currentMode = mode
            self.eventMap["ModeSwitchEvent"].setMode(mode)
            self.dispatchEvent(self.eventMap["ModeSwitchEvent"])
            return

        if self.__awaitingSeed:
            try:
                seed = float(userInput)
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
                self.__triggerExit()
            operands.append(userInput)

        self.eventMap["RecieveDataEvent"].setData(operands)
        self.dispatchEvent(self.eventMap["RecieveDataEvent"])

    # ==================================================
    # POST-RESULT
    # ==================================================

    def __requestContinue(self):
        self.__requestOperation()

    # ==================================================
    # KEEP PROMPTS
    # ==================================================

    def __requestKeepScientific(self):
        if self.__lastResult is None:
            self.__requestContinue()
            return

        saved = input("¿Quieres conservar este resultado? S/N\n").strip().lower()

        if saved == Operations.EXIT.value:
            self.__triggerExit()
        if saved == "s":
            op = input("¿Qué operación quieres aplicar? +, -, x, /\n").strip().lower()
            operation = self.__strToBaseOperation(op)
            if operation is None:
                print("Operación no válida. Resultado descartado.")
                self.__requestContinue()
                return
            self.eventMap["KeepResultEvent"].setOperation(operation)
            self.eventMap["KeepResultEvent"].setValue(self.__lastResult)
            self.dispatchEvent(self.eventMap["KeepResultEvent"])
        else:
            print("Resultado descartado.")
            self.__requestContinue()

    def __requestKeepSecondDegree(self):
        if self.__lastResult is None:
            self.__requestContinue()
            return

        x1, x2 = self.__lastResult
        saved = input("¿Conservar algún resultado? x1/x2/N\n").strip().lower()

        if saved == Operations.EXIT.value:
            self.__triggerExit()
        if saved == "x1":
            chosen = x1
        elif saved == "x2":
            chosen = x2
        else:
            print("Resultado descartado.")
            self.__requestContinue()
            return

        if chosen is None:
            print("Ese resultado no existe. Descartado.")
            self.__requestContinue()
            return

        op = input("¿Qué operación quieres aplicar? +, -, x, /\n").strip().lower()
        operation = self.__strToBaseOperation(op)
        if operation is None:
            print("Operación no válida. Resultado descartado.")
            self.__requestContinue()
            return

        self.eventMap["KeepResultEvent"].setOperation(operation)
        self.eventMap["KeepResultEvent"].setValue(chosen)
        self.dispatchEvent(self.eventMap["KeepResultEvent"])

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

    def __strToBaseOperation(self, operation):
        match operation:
            case Operations.ADD.value:      return Operations.ADD
            case Operations.SUBTRACT.value: return Operations.SUBTRACT
            case Operations.MULTIPLY.value: return Operations.MULTIPLY
            case Operations.DIVIDE.value:   return Operations.DIVIDE
            case _:                         return None