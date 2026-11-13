from libr.UtilLibrary.AbstractController import AbstractController
from libr.UtilLibrary.Subscriber import Subscriber

from multipledispatch import dispatch

from src.event.UpdateDataEvent import UpdateDataEvent

from src.Init import EventType
from src.Init import Modes


class DisplayOutputController(AbstractController, Subscriber):

    def __init__(self):
        AbstractController.__init__(self)
        Subscriber.__init__(self)

    def setAsociatedViews(self, terminalView):
        self.terminalView = terminalView

    def setAsociatedModels(self, displayOutputModel):
        self.displayOutputModel = displayOutputModel

    @dispatch(UpdateDataEvent)
    def onEventReceived(self, event):

        eventType = event.getType()
        step = event.getStep()
        data = event.getData()

        self.displayOutputModel.setText(eventType, data)

        currentMode = None
        if isinstance(eventType, Modes):
            currentMode = eventType

        if step in (EventType.DATA, EventType.RESULT):
            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step,
                data,
                currentMode,
                eventType
            )
        else:
            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step,
                1,
                currentMode,
                eventType
            )