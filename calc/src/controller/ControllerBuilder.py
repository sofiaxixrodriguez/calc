from libr.UtilLibrary.Singleton import SingletonMeta
from libr.UtilLibrary.ObjectBuilder import ObjectBuilder

from src.controller.DisplayOutputController import DisplayOutputController
from src.controller.ExecuteOperationController import ExecuteOperationController
from src.controller.SelectModeController import SelectModeController

class ControllerBuilder(ObjectBuilder, metaclass=SingletonMeta):
    def __init__(self):
        ObjectBuilder.__init__(self)
        self.elementsMap: dict = {
                "DisplayOutputController": DisplayOutputController(),
                "ExecuteOperationController": ExecuteOperationController(),
                "SelectModeController": SelectModeController()
        }

