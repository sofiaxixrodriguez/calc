
from libr.UtilLibrary.LinkElementsInterface import LinkElementsInterface
from src.controller.ControllerBuilder import ControllerBuilder
from src.event.EventBuilder import EventBuilder
from src.model.ModelBuilder import ModelBuilder
from src.view.ViewBuilder import ViewBuilder


class LinkElements(LinkElementsInterface):
    def __init__(self, mainWindow):
        LinkElementsInterface.__init__(self)
        self.modelBuilder = ModelBuilder()
        self.viewBuilder = ViewBuilder(mainWindow)
        self.controllerBuilder = ControllerBuilder()
        self.eventBuilder = EventBuilder()

    def linkControllers(self):
        self.controllerBuilder.getElement(''). \
            setAsociatedViews(self.viewBuilder.getElement(''))
        self.controllerBuilder.getElement(''). \
            setAsociatedModels(self.modelBuilder.getElement(''))

    def linkViews(self):
        self.viewBuilder.getElement(''). \
            setAsociatedModels(self.modelBuilder.getElement(''))
        self.viewBuilder.getElement(('')). \
            addEvent(self.eventBuilder.getElement(''))

    def linkModels(self):
        self.modelBuilder.getElement(('')). \
            addEvent(self.eventBuilder.getElement(''))

    def registerEvents(self):
        self.eventBuilder.getElement(''). \
            register(self.controllerBuilder.getElement(''))
        self.eventBuilder.getElement(''). \
            register(self.viewBuilder.getElement(''))

    def initElements(self):
        pass
