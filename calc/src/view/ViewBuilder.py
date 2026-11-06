
from libr.UtilLibrary.Singleton import SingletonMeta
from libr.UtilLibrary.ObjectBuilder import ObjectBuilder

from src.view.TerminalView import TerminalView

class ViewBuilder(ObjectBuilder, metaclass=SingletonMeta):
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        ObjectBuilder.__init__(self)
        self.elementsMap: dict = {
            "TerminalView": TerminalView()
        }
