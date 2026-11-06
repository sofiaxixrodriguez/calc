from libr.UtilLibrary.AbstractController import AbstractController
from libr.UtilLibrary.Subscriber import Subscriber

from multipledispatch import dispatch

from src.event.ExecuteOperationEvent import ExecuteOperationEvent
from src.event.RecieveDataEvent import RecieveDataEvent

from src.Init import Operations


class ExecuteOperationController(AbstractController, Subscriber):

    def __init__(self):
        AbstractController.__init__(self)
        Subscriber.__init__(self)

        self.__currentOperation = Operations.NONE

    # ==================================================
    # MVC LINKS
    # ==================================================

    def setAsociatedViews(self, *args):
        pass

    def setAsociatedModels(
        self,
        executeOperationModel,
        displayOutputModel
    ):
        self.executeOperationModel = executeOperationModel
        self.displayOutputModel = displayOutputModel

    # ==================================================
    # OPERATION SELECTION
    # ==================================================

    @dispatch(ExecuteOperationEvent)
    def onEventReceived(self, event):

        self.__currentOperation = event.getOperation()

        self.executeOperationModel.setOperation(
            self.__currentOperation
        )

    # ==================================================
    # DATA RECEPTION
    # ==================================================

    @dispatch(RecieveDataEvent)
    def onEventReceived(self, event):

        rawData = event.getData()

        parsedData = self.__parseData(
            self.__currentOperation,
            rawData
        )

        if parsedData is None:
            return

        self.executeOperationModel.execute(
            self.__currentOperation,
            parsedData
        )

    # ==================================================
    # INPUT PARSING
    # ==================================================

    def __parseData(self, operation, data):

        try:

            match operation:

                # -------------------------
                # BASE OPERATIONS
                # -------------------------

                case Operations.ADD:
                    return [float(data[0])]

                case Operations.SUBTRACT:
                    return [float(data[0])]

                case Operations.MULTIPLY:
                    return [float(data[0])]

                case Operations.DIVIDE:
                    return [float(data[0])]

                # -------------------------
                # SCIENTIFIC
                # -------------------------

                case Operations.POWER:

                    return [
                        float(data[0]),
                        float(data[1])
                    ]

                case Operations.FACTORIAL:

                    return [
                        float(data[0])
                    ]

                case Operations.SQUARE_ROOT:

                    return [
                        float(data[0])
                    ]

                case Operations.SECOND_DEGREE:

                    return [
                        float(data[0]),
                        float(data[1]),
                        float(data[2])
                    ]

                # -------------------------
                # PROGRAMMING
                # -------------------------

                case Operations.DECIMAL_TO_HEX:

                    return [
                        float(data[0])
                    ]

                case _:

                    return None

        except ValueError:

            self.executeOperationModel.eventMap[
                "UpdateDataEvent"
            ].setData(
                "INVALID_NUMBER"
            )

            self.executeOperationModel.eventMap[
                "UpdateDataEvent"
            ].notifyAll()

            return None