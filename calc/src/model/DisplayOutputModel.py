from libr.UtilLibrary.AbstractModel import AbstractModel
from libr.UtilLibrary.Publisher import Publisher
from src.Init import Modes, Operations, OutputType


class DisplayOutputModel(AbstractModel, Publisher):

    def __init__(self):
        AbstractModel.__init__(self)
        Publisher.__init__(self)
        self.parseData()

    def parseData(self):
        self.__text = ""
        self.__currentMode = Modes.BASE

    def setText(self, eventType, data):

        # Initial main menu (eventType is None)
        if eventType is None:
            self.__text = (
                "Modos disponibles:\n"
                "\tBASE -> base\n"
                "\tCIENTÍFICA -> cien\n"
                "\tPROGRAMACIÓN -> prog\n"
                "\nIntroduce un número para empezar, un modo para cambiar,"
                " o '=' para salir.\n"
            )
            return

        # A mode was selected -> show its operations menu
        if isinstance(eventType, Modes):
            self.__currentMode = eventType
            self.__text = self.__modeMenu(eventType)
            return

        # "Return to operation prompt" (used after seeding)
        if eventType == OutputType.MAIN_MENU:
            self.__text = self.__modeMenu(self.__currentMode)
            return

        # An operation was selected (data is either operand count or error string)
        if isinstance(eventType, Operations):
            if isinstance(data, str) and data == "INVALID_NUMBER":
                self.__text = "Número inválido. Intenta de nuevo:"
            else:
                self.__text = self.__operationPrompt(eventType)
            return

        # Result of a computation
        if eventType == OutputType.RESULT:
            if data is None:
                self.__text = "Error: la operación no produjo un resultado válido."
            else:
                self.__text = f"[Resultado actual: {data}]"

    def getText(self):
        return self.__text

    def __modeMenu(self, mode):
        match mode:
            case Modes.BASE:
                return (
                    "Modo: BASE\nOperaciones permitidas:\n"
                    "\tSUMA -> +\n\tRESTA -> -\n"
                    "\tMULTIPLICACIÓN -> x\n\tDIVISIÓN -> /\n"
                )
            case Modes.SCIENTIFIC:
                return (
                    "Modo: CIENTÍFICA\nOperaciones permitidas:\n"
                    "\tPOTENCIA -> p\n\tFACTORIAL -> f\n"
                    "\tRAÍZ CUADRADA -> r\n\tECUACIÓN 2do GRADO -> s\n"
                )
            case Modes.PROGRAMMING:
                return (
                    "Modo: PROGRAMACIÓN\nOperaciones permitidas:\n"
                    "\tCONVERSIÓN HEXADECIMAL -> hex\n"
                )
        return ""

    def __operationPrompt(self, operation):
        match operation:
            case Operations.ADD:            return "Introduce el sumando:"
            case Operations.SUBTRACT:       return "Introduce el sustraendo:"
            case Operations.MULTIPLY:       return "Introduce el factor:"
            case Operations.DIVIDE:         return "Introduce el divisor:"
            case Operations.POWER:          return "Introduce base y exponente (uno por línea):"
            case Operations.FACTORIAL:      return "Introduce el número para factorial:"
            case Operations.SQUARE_ROOT:    return "Introduce el número para raíz cuadrada:"
            case Operations.SECOND_DEGREE:  return "Introduce a, b, c (uno por línea):"
            case Operations.DECIMAL_TO_HEX: return "Introduce el entero positivo a convertir:"
        return "Introduce datos:"