from enum import Enum, auto

class KettleTelemetry(Enum):
    waterTemperature = auto()
    waterLevel = auto()
    waterLevelPercent =auto
    waterHeatingProgress = auto()
    isHeating = auto()
    
class KettleAttributes(Enum):
    firmware = auto(),
    waterVolume = auto()
class RpcCommands(Enum):
    fillWater = auto()
    setState = auto()