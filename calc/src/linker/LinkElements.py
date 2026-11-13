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

    def linkControllers(self):
        displayCtrl = self.controllerBuilder.getElement("DisplayOutputController")
        displayCtrl.setAsociatedViews(
            self.viewBuilder.getElement("TerminalView")
        )
        displayCtrl.setAsociatedModels(
            self.modelBuilder.getElement("DisplayOutputModel")
        )

        execCtrl = self.controllerBuilder.getElement("ExecuteOperationController")
        execCtrl.setAsociatedModels(
            self.modelBuilder.getElement("ExecuteOperationModel"),
            self.modelBuilder.getElement("DisplayOutputModel")
        )

        self.controllerBuilder.getElement("SelectModeController").setAsociatedModels(
            self.modelBuilder.getElement("SelectModeModel")
        )

    def linkViews(self):
        terminalView = self.viewBuilder.getElement("TerminalView")
        terminalView.addEvent(
            self.eventBuilder.getElement("ModeSwitchEvent"),
            self.eventBuilder.getElement("ExecuteOperationEvent"),
            self.eventBuilder.getElement("RecieveDataEvent"),
            self.eventBuilder.getElement("SeedEvent"),
            self.eventBuilder.getElement("ExitEvent"),
            self.eventBuilder.getElement("KeepResultEvent")
        )

    def linkModels(self):
        updateEvent = self.eventBuilder.getElement("UpdateDataEvent")
        for modelName in ("DisplayOutputModel",
                          "ExecuteOperationModel",
                          "SelectModeModel"):
            self.modelBuilder.getElement(modelName).addEvent(updateEvent)

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
        self.eventBuilder.getElement("ExitEvent").register(
            self.controllerBuilder.getElement("ExecuteOperationController")
        )
        self.eventBuilder.getElement("KeepResultEvent").register(
            self.controllerBuilder.getElement("ExecuteOperationController")
        )
        self.eventBuilder.getElement("UpdateDataEvent").register(
            self.controllerBuilder.getElement("DisplayOutputController")
        )

    def initElements(self):
        updateEvent = self.eventBuilder.getElement("UpdateDataEvent")
        updateEvent.setStep(EventType.MODE)
        updateEvent.setType(None)
        updateEvent.setData(None)
        updateEvent.notifyAll()