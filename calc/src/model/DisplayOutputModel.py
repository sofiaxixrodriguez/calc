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

        # ------------------------------------------------------
        # Initial screen: mode list + default BASE menu
        # ------------------------------------------------------
        if eventType is None:
            self.__text = (
                "Modos disponibles:\n"
                "\tBASE -> base\n"
                "\tCIENTÍFICA -> cien\n"
                "\tPROGRAMACIÓN -> prog\n"
                "\n"
                "Modo: BASE\n"
                "Operaciones permitidas:\n"
                "\tSUMA -> +\n"
                "\tRESTA -> -\n"
                "\tMULTIPLICACIÓN -> x\n"
                "\tDIVISIÓN -> /\n"
                "\n"
                "Introduce un número para empezar, un modo para cambiar,"
                " o '=' para salir.\n"
            )
            return

        # ------------------------------------------------------
        # Mode switch -> show its operations menu
        # ------------------------------------------------------
        if isinstance(eventType, Modes):
            self.__currentMode = eventType
            self.__text = self.__modeMenu(eventType)
            return

        # ------------------------------------------------------
        # Operation selection (data is operand count or "INVALID_NUMBER")
        # ------------------------------------------------------
        if isinstance(eventType, Operations):
            if isinstance(data, str) and data == "INVALID_NUMBER":
                self.__text = "Número inválido. Intenta de nuevo:"
            else:
                self.__text = self.__operationPrompt(eventType)
            return

        # ------------------------------------------------------
        # Accumulator result (seed, + - x /)
        # ------------------------------------------------------
        if eventType == OutputType.RESULT:
            if data is None:
                self.__text = "Error: la operación no produjo un resultado válido."
            else:
                self.__text = f"[Resultado actual: {data}]"
            return

        # ------------------------------------------------------
        # Scientific result (p, f, r) — not the accumulator
        # ------------------------------------------------------
        if eventType == OutputType.SCIENTIFIC_RESULT:
            if data is None:
                self.__text = "Error: la operación no produjo un resultado válido."
            else:
                self.__text = f"[Resultado: {data}]"
            return

        # ------------------------------------------------------
        # Second-degree (s) — not the accumulator
        # ------------------------------------------------------
        if eventType == OutputType.SECOND_DEGREE_RESULT:
            if data is None:
                self.__text = "La ecuación no tiene soluciones reales."
            else:
                x1, x2 = data
                self.__text = f"[Resultado: x1 = {x1}, x2 = {x2}]"
            return

        # ------------------------------------------------------
        # Hex conversion: data is (original_value, hex_string)
        # ------------------------------------------------------
        if eventType == OutputType.HEX_RESULT:
            if data is None:
                self.__text = "Error en la conversión."
            else:
                orig, hex_str = data
                if hex_str is None:
                    self.__text = "Error: solo se permiten enteros positivos."
                else:
                    self.__text = (
                        f"El número {int(orig)} en hexadecimal es: {hex_str}\n"
                        f"(Operación informativa: el valor actual no se modifica)"
                    )
            return

        # ------------------------------------------------------
        # Final result (on '=')
        # ------------------------------------------------------
        if eventType == OutputType.FINAL_RESULT:
            self.__text = f"Resultado final: {data}"
            return

    def getText(self):
        return self.__text

    # ==================================================
    # MENUS
    # ==================================================

    def __modeMenu(self, mode):
        match mode:
            case Modes.BASE:
                return (
                    "Modo: BASE\n"
                    "Operaciones permitidas:\n"
                    "\tSUMA -> +\n"
                    "\tRESTA -> -\n"
                    "\tMULTIPLICACIÓN -> x\n"
                    "\tDIVISIÓN -> /\n"
                )
            case Modes.SCIENTIFIC:
                return (
                    "Modo: CIENTÍFICA\n"
                    "Operaciones permitidas:\n"
                    "\tPOTENCIA -> p\n"
                    "\tFACTORIAL -> f\n"
                    "\tRAÍZ CUADRADA -> r\n"
                    "\tECUACIÓN 2do GRADO -> s\n"
                )
            case Modes.PROGRAMMING:
                return (
                    "Modo: PROGRAMACIÓN\n"
                    "Operaciones permitidas:\n"
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