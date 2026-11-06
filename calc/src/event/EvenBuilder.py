
from libr.UtilLibrary.Singleton import SingletonMeta
from libr.UtilLibrary.ObjectBuilder import ObjectBuilder

from src.event.ExecuteOperationEvent import ExecuteOperationEvent
from src.event.ModeSwitchEvent import ModeSwitchEvent
from src.event.RecieveDataEvent import RecieveDataEvent
from src.event.UpdateDataEvent import UpdateDataEvent

class EventBuilder(ObjectBuilder, metaclass=SingletonMeta):
    def __init__(self):
        ObjectBuilder.__init__(self)
        self.elementsMap: dict = {
            "ExecuteOperationEvent": ExecuteOperationEvent(),
            "ModeSwitchEvent": ModeSwitchEvent(),
            "RecieveDataEvent": RecieveDataEvent(),
            "UpdateDataEvent": UpdateDataEvent()
        }
