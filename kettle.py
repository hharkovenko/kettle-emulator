from enums import KettleAttributes, KettleTelemetry


BOILED_TEMPERATURE = 100  
BASE_TEMPERATURE = 25
MAX_WATER_VOLUME = 1500

class Kettle:
    def __init__(self):
        self.isHeating = False
        self.waterLevel = 0
        self.waterTemperature = BASE_TEMPERATURE
        self.waterHeatingProgress=0
    def get_current_telemetry(self):
        return {KettleTelemetry.waterTemperature.name : self.waterTemperature,
                 KettleTelemetry.waterLevel.name: self.waterLevel, 
                 KettleTelemetry.waterHeatingProgress.name : self.waterHeatingProgress,
                 KettleTelemetry.isHeating.name : self.isHeating}
    def get_attributes(self):
        return {
        KettleAttributes.firmware.name : "1.0.0",
        KettleAttributes.waterVolume.name : MAX_WATER_VOLUME
    }
    def fill_water(self, amount):
        self.waterLevel = amount
    def power(self, state):
        self.isHeating = state
        if self.isHeating:
            print("Heating started...")
        else:
            print("Heating stopped.")
    def update_heating(self):
        """Simulate heating and cooling with realistic dynamics."""
     
        # Heating logic
        if  self.isHeating and  self.waterHeatingProgress < 100:
            # The closer to 100°C, the faster it heats
            heat_rate = ( self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE + 0.001)  
            # minimum 0.2 °C/sec, maximum 2.0 °C/sec
            temp_step = max(10, 10.0 * heat_rate)  

            self.waterTemperature += temp_step
            self.waterHeatingProgress = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE) * 100

            if  self.waterTemperature >= BOILED_TEMPERATURE:
                self.waterTemperature = BOILED_TEMPERATURE
                self.waterHeatingProgress = 100
                self.power(False)
                print("Heating complete.")

        # Cooling logic
        elif not self.isHeating and self.waterTemperature > BASE_TEMPERATURE:
            # Faster cooling when hotter
            cool_rate = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE)  
            # minimum 0.1 °C/sec, maximum 1.5 °C/sec
            cool_step = max(7, 8 * cool_rate)

            self.waterTemperature -= cool_step
            self.waterHeatingProgress = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE) * 100

            if self.waterTemperature <= BASE_TEMPERATURE:
                self.waterTemperature = BASE_TEMPERATURE
                self.waterHeatingProgress = 0
                print("Cooling complete.")