from libr.UtilLibrary.LinkElementsInterface import LinkElementsInterface

from src.controller.ControllerBuilder import ControllerBuilder
from src.event.EventBuilder import EventBuilder
from src.model.ModelBuilder import ModelBuilder
from src.view.ViewBuilder import ViewBuilder

from src.Init import EventType


class LinkElements(LinkElementsInterface):

    def __init__(self, mainWindow):
        LinkElementsInterface.__init__(self)
        self.modelBuilder = ModelBuilder()
        self.viewBuilder = ViewBuilder(mainWindow)
        self.controllerBuilder = ControllerBuilder()
        self.eventBuilder = EventBuilder()

    # ==================================================
    # CONTROLLER -> VIEWS / MODELS
    # ==================================================
    def linkControllers(self):
        # DisplayOutputController sees the view and the display model
        displayCtrl = self.controllerBuilder.getElement("DisplayOutputController")
        displayCtrl.setAsociatedViews(
            self.viewBuilder.getElement("TerminalView")
        )
        displayCtrl.setAsociatedModels(
            self.modelBuilder.getElement("DisplayOutputModel")
        )

        # ExecuteOperationController needs the operation model
        execCtrl = self.controllerBuilder.getElement("ExecuteOperationController")
        execCtrl.setAsociatedModels(
            self.modelBuilder.getElement("ExecuteOperationModel"),
            self.modelBuilder.getElement("DisplayOutputModel")
        )

        # SelectModeController needs the mode model
        self.controllerBuilder.getElement("SelectModeController").setAsociatedModels(
            self.modelBuilder.getElement("SelectModeModel")
        )

    # ==================================================
    # VIEW -> MODELS / EVENTS
    # ==================================================
    def linkViews(self):
        terminalView = self.viewBuilder.getElement("TerminalView")
        terminalView.addEvent(
            self.eventBuilder.getElement("ModeSwitchEvent"),
            self.eventBuilder.getElement("ExecuteOperationEvent"),
            self.eventBuilder.getElement("RecieveDataEvent"),
            self.eventBuilder.getElement("SeedEvent")
        )

    # ==================================================
    # MODELS -> EVENTS
    # ==================================================
    def linkModels(self):
        updateEvent = self.eventBuilder.getElement("UpdateDataEvent")

        for modelName in ("DisplayOutputModel",
                          "ExecuteOperationModel",
                          "SelectModeModel"):
            self.modelBuilder.getElement(modelName).addEvent(updateEvent)

    # ==================================================
    # EVENT -> SUBSCRIBERS
    # ==================================================
    def registerEvents(self):
        self.eventBuilder.getElement("ModeSwitchEvent").register(
            self.controllerBuilder.getElement("SelectModeController")
        )
        self.eventBuilder.getElement("ExecuteOperationEvent").register(
            self.controllerBuilder.getElement("ExecuteOperationController")
        )
        self.eventBuilder.getElement("RecieveDataEvent").register(
            self.controllerBuilder.getElement("ExecuteOperationController")
        )
        self.eventBuilder.getElement("SeedEvent").register(
            self.controllerBuilder.getElement("ExecuteOperationController")
        )
        self.eventBuilder.getElement("UpdateDataEvent").register(
            self.controllerBuilder.getElement("DisplayOutputController")
        )

    # ==================================================
    # KICK-OFF
    # ==================================================
    def initElements(self):
        updateEvent = self.eventBuilder.getElement("UpdateDataEvent")
        updateEvent.setStep(EventType.MODE)
        updateEvent.setType(None)
        updateEvent.setData(None)
        updateEvent.notifyAll()