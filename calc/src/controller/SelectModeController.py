from libr.UtilLibrary.AbstractController import AbstractController
from libr.UtilLibrary.Subscriber import Subscriber

from multipledispatch import dispatch

from src.event.ModeSwitchEvent import ModeSwitchEvent


class SelectModeController(AbstractController, Subscriber):

    def __init__(self):
        AbstractController.__init__(self)
        Subscriber.__init__(self)

    # ==========================================
    # MVC LINKS
    # ==========================================

    def setAsociatedViews(self, *args):
        pass

    def setAsociatedModels(self, selectModeModel):
        self.selectModeModel = selectModeModel

    # ==========================================
    # EVENT HANDLING
    # ==========================================

    @dispatch(ModeSwitchEvent)
    def onEventReceived(self, event):

        self.selectModeModel.setMode(
            event.getMode()
        )