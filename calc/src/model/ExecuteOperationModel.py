from libr.UtilLibrary.Publisher import Publisher
from libr.UtilLibrary.AbstractModel import AbstractModel

from src.Init import Operations
from src.Init import EventType
from src.Init import OutputType


class ExecuteOperationModel(AbstractModel, Publisher):

    def __init__(self):
        AbstractModel.__init__(self)
        Publisher.__init__(self)

        self.parseData()

    def parseData(self):

        self.__result = 0.0
        self.__operation = Operations.NONE

    # ==================================================
    # GETTERS / SETTERS
    # ==================================================

    def getResult(self):
        return self.__result

    def setResult(self, value):
        self.__result = value

    def getOperation(self):
        return self.__operation

    def setOperation(self, operation):

        self.__operation = operation

        self.eventMap["UpdateDataEvent"].setStep(
            EventType.DATA
        )

        self.eventMap["UpdateDataEvent"].setType(
            operation
        )

        self.eventMap["UpdateDataEvent"].setData(
            self.numberOfOperandsNeeded(operation)
        )

        self.dispatchEvent(
            self.eventMap["UpdateDataEvent"]
        )

    # ==================================================
    # OPERAND COUNT
    # ==================================================

    def numberOfOperandsNeeded(self, operation):

        match operation:

            case Operations.ADD:
                return 1

            case Operations.SUBTRACT:
                return 1

            case Operations.MULTIPLY:
                return 1

            case Operations.DIVIDE:
                return 1

            case Operations.POWER:
                return 2

            case Operations.FACTORIAL:
                return 1

            case Operations.SQUARE_ROOT:
                return 1

            case Operations.SECOND_DEGREE:
                return 3

            case Operations.DECIMAL_TO_HEX:
                return 1

            case _:
                return 0

    # ==================================================
    # BASE OPERATIONS
    # ==================================================

    def add(self, value):
        self.__result += value
        return self.__result

    def subtract(self, value):
        self.__result -= value
        return self.__result

    def multiply(self, value):
        self.__result *= value
        return self.__result

    def divide(self, value):

        if value == 0:
            return None

        self.__result /= value
        return self.__result

    # ==================================================
    # SCIENTIFIC
    # ==================================================

    def factorial(self, value):

        if value < 0:
            return None

        result = 1

        current = int(value)

        while current >= 1:
            result *= current
            current -= 1

        return float(result)

    def power(self, base, exponent):

        result = 1

        exponent = int(exponent)

        while exponent > 0:
            result *= base
            exponent -= 1

        return float(result)

    def squareRoot(self, value):

        if value < 0:
            return None

        if value == 0:
            return 0.0

        root = 1.0

        while True:

            tempRoot = round(
                ((root + (value / root)) / 2),
                3
            )

            if abs(root - tempRoot) < 0.0001:
                return tempRoot

            root = tempRoot

    # ==================================================
    # SECOND DEGREE EQUATION
    # ==================================================

    def _missingB(self, a, c):

        x = self.squareRoot(-c / a)

        if x is None:
            return None

        return (-round(x, 3), round(x, 3))

    def _missingC(self, a, b):

        return (0.0, round(-b / a, 3))

    def _missingA(self, b, c):

        if b == 0:
            return None

        return (round(-c / b, 3), None)

    def secondDegreeEquation(self, a, b, c):

        if a == 0:
            return self._missingA(b, c)

        if b == 0:
            return self._missingB(a, c)

        if c == 0:
            return self._missingC(a, b)

        discriminant = (b * b) - (4 * a * c)

        if discriminant < 0:
            return None

        x1 = round(
            (-b + self.squareRoot(discriminant)) / (2 * a),
            3
        )

        x2 = round(
            (-b - self.squareRoot(discriminant)) / (2 * a),
            3
        )

        return (x1, x2)

    # ==================================================
    # PROGRAMMING
    # ==================================================

    def decimalToHex(self, value):

        if value < 0:
            return None

        value = int(value)

        if value == 0:
            return "0"

        chars = "0123456789ABCDEF"

        result = ""

        while value > 0:

            result = chars[value % 16] + result

            value //= 16

        return result

    # ==================================================
    # EXECUTION
    # ==================================================

    def execute(self, operation, data):

        result = None

        match operation:

            case Operations.ADD:
                result = self.add(data[0])

            case Operations.SUBTRACT:
                result = self.subtract(data[0])

            case Operations.MULTIPLY:
                result = self.multiply(data[0])

            case Operations.DIVIDE:
                result = self.divide(data[0])

            case Operations.POWER:
                result = self.power(
                    data[0],
                    data[1]
                )

            case Operations.FACTORIAL:
                result = self.factorial(
                    data[0]
                )

            case Operations.SQUARE_ROOT:
                result = self.squareRoot(
                    data[0]
                )

            case Operations.SECOND_DEGREE:
                result = self.secondDegreeEquation(
                    data[0],
                    data[1],
                    data[2]
                )

            case Operations.DECIMAL_TO_HEX:
                result = self.decimalToHex(
                    data[0]
                )

        self.eventMap["UpdateDataEvent"].setStep(
            EventType.RESULT
        )

        self.eventMap["UpdateDataEvent"].setType(
            OutputType.RESULT
        )

        self.eventMap["UpdateDataEvent"].setData(
            result
        )

        self.dispatchEvent(
            self.eventMap["UpdateDataEvent"]
        )

        return result