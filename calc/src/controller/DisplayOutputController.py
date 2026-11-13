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

        # A mode was selected -> surface it to the view so it can
        # remember the current mode for "return to operation prompt"
        currentMode = None

        if isinstance(eventType, Modes):
            currentMode = eventType

        # DATA events carry the operand count (int).
        # RESULT events carry the actual result (float / tuple / str / None).
        # Both must be forwarded verbatim — not replaced by a placeholder.
        if step in (EventType.DATA, EventType.RESULT):

            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step,
                data,
                currentMode
            )

        # MODE / OPERATION / MESSAGE events have nothing extra to forward,
        # so pass a neutral operand count of 1.
        else:

            self.terminalView.setText(
                self.displayOutputModel.getText(),
                step,
                1,
                currentMode
            )