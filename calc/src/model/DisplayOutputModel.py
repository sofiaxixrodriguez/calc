from libr.UtilLibrary.AbstractController import AbstractController
from libr.UtilLibrary.Subscriber import Subscriber

from multipledispatch import dispatch

from src.event.UpdateDataEvent import UpdateDataEvent
from src.Init import EventType


class DisplayOutputController(AbstractController, Subscriber):

    def __init__(self):
        AbstractController.__init__(self)
        Subscriber.__init__(self)

    # ==================================================
    # MVC LINKS
    # ==================================================

    def setAsociatedViews(self, terminalView):
        self.terminalView = terminalView

    def setAsociatedModels(self, displayOutputModel):
        self.displayOutputModel = displayOutputModel

    # ==================================================
    # EVENT HANDLING
    # ==================================================

    @dispatch(UpdateDataEvent)
    def onEventReceived(self, event):

        eventType = event.getType()
        step = event.getStep()
        data = event.getData()

        # DisplayOutputModel owns ALL text
        self.displayOutputModel.setText(
            eventType,
            data
        )

        # DATA events need operand count
        if step == EventType.DATA:

            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step,
                data
            )

        else:

            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step
            )