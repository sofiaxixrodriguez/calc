
from libr.UtilLibrary.Singleton import SingletonMeta
from libr.UtilLibrary.ObjectBuilder import ObjectBuilder

from src.model.DisplayOutputModel import DisplayOutputModel
from src.model.ExecuteOperationModel import ExecuteOperationModel
from src.model.SelectModeModel import SelectModeModel

class ModelBuilder(ObjectBuilder, metaclass=SingletonMeta):
    def __init__(self):
        ObjectBuilder.__init__(self)
        self.elementsMap: dict = {
            "DisplayOutputModel": DisplayOutputModel(),
            "ExecuteOperationModel": ExecuteOperationModel(),
            "SelectModeModel": SelectModeModel()
        }
