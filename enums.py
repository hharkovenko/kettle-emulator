from enum import Enum, auto

class KettleTelemetry(Enum):
    waterTemperature = auto()
    waterLevel = auto()
    waterHeatingProgress = auto()
    isHeating = auto()
    
class KettleAttributes(Enum):
    firmware = auto(),
    waterVolume = auto()