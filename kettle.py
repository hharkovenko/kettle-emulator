from threading import Thread
import time
from enums import KettleAttributes, KettleTelemetry


BOILED_TEMPERATURE = 100  
BASE_TEMPERATURE = 25
MAX_WATER_VOLUME = 1500
MIN_TEMPERATURE_STEP = 1
MAX_TEMPERATURE_STEP = 3
class Kettle:
    def __init__(self):
        self.isHeating = False
        self.waterLevel = 0
        self.waterLevelPercent = 0
        self.waterTemperature = BASE_TEMPERATURE
        self.waterHeatingProgressPercent=0
        self.isRunning = True
        self.thread = Thread(target=self.work)
        self.thread.start()
    def stop(self):
        self.isRunning = False
        print('kettle stop')
        self.thread.join()
        
    def work(self):
        while self.isRunning:
            self.update_state()
            time.sleep(3)
    def get_current_telemetry(self):
        return {KettleTelemetry.waterTemperature.name : self.waterTemperature,
                 KettleTelemetry.waterLevel.name: self.waterLevel, 
                 KettleTelemetry.waterLevelPercent.name : self.waterLevelPercent,
                 KettleTelemetry.waterHeatingProgress.name : self.waterHeatingProgressPercent,
                 KettleTelemetry.isHeating.name : self.isHeating}
    def get_attributes(self):
        return {
        KettleAttributes.firmware.name : "1.0.0",
        KettleAttributes.waterVolume.name : MAX_WATER_VOLUME
    }
    def fill_water(self, amount):
        self.waterLevel = amount * MAX_WATER_VOLUME / 100
        self.waterLevelPercent = amount
    def power(self, state):
        self.isHeating = state
        if self.isHeating:
            print("Heating started...")
        else:
            print("Heating stopped.")
    def cool(self):
         # Faster cooling when hotter
            cool_rate = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE)  
            # minimum 0.1 °C/sec, maximum 1.5 °C/sec
            cool_step = max(MIN_TEMPERATURE_STEP, MAX_TEMPERATURE_STEP * cool_rate)
            self.waterTemperature -= cool_step
            self.waterHeatingProgressPercent = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE) * 100
            if self.waterTemperature <= BASE_TEMPERATURE:
                self.waterTemperature = BASE_TEMPERATURE
                self.waterHeatingProgressPercent = 0
                print("Cooling complete.")
    def heat(self):
        # The closer to 100°C, the faster it heats
            heat_rate = ( self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE + 0.001)  
            temp_step = max(MIN_TEMPERATURE_STEP, MAX_TEMPERATURE_STEP * heat_rate)  
            self.waterTemperature += temp_step
            self.waterHeatingProgressPercent = (self.waterTemperature - BASE_TEMPERATURE) / (BOILED_TEMPERATURE - BASE_TEMPERATURE) * 100
            if  self.waterTemperature >= BOILED_TEMPERATURE:
                self.waterTemperature = BOILED_TEMPERATURE
                self.waterHeatingProgressPercent = 100
                self.power(False)
                print("Heating complete.")
    def update_state(self):
        """Simulate heating and cooling with realistic dynamics."""
        # Heating logic
        if  self.isHeating and  self.waterHeatingProgressPercent < 100:
            self.heat()
        # Cooling logic
        elif not self.isHeating and self.waterTemperature > BASE_TEMPERATURE:
           self.cool()