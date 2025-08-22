from enum import Enum
import paho.mqtt.client as mqtt
import json
import time

from enums import KettleTelemetry, KettleAttributes, RpcCommands
from kettle import Kettle

# Replace with your ThingsBoard instance host
THINGSBOARD_HOST = "demo.thingsboard.io"
#Replace with your device access token
ACCESS_TOKEN = ""

RPC_SUBSCRIPTION_URL = 'v1/devices/me/rpc/request/+'

class Emulator:
    def __init__(self, kettle: Kettle, client : mqtt.Client,):
        self.kettle = kettle
        self.client = client
        self.start()
        
    def on_set_state(self,value: bool):
        self.kettle.power(value)

    def on_fill_water(self,amount:int):
        self.kettle.fill_water(amount)
    #handle rpc call from platform
    def on_rpc_method(self, method, value):
        if(method == RpcCommands.setState.name):
            self.on_set_state(value)
            return
        if(method == RpcCommands.fillWater.name):
            self.on_fill_water(value)
            return
    # Callback when connected
    def on_connect(self,client : mqtt.Client, userdata, flags, rc, properties=None):
        print("Connected with result code " + str(rc))
        # Subscribe to RPC requests
        client.subscribe(RPC_SUBSCRIPTION_URL)    

    # Callback when message received
    def on_message(self, client: mqtt.Client, userData, msg:mqtt.MQTTMessage):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        try:
            data = json.loads(msg.payload.decode())
            if msg.topic.startswith("v1/devices/me/rpc/request/"):
                request_id = msg.topic.split("/")[-1]
                method = data.get("method")
                params = data.get("params")
                self.on_rpc_method(method, params)
        except Exception as e:
            print("Error processing message:", e)
            
    def send_telemetry(self):
        telemetry = self.kettle.get_current_telemetry()
        self.client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
        print("Telemetry sent:", telemetry)
        
    def send_attributes(self):
        attributes = self.kettle.get_attributes()
        self.client.publish("v1/devices/me/attributes", json.dumps(attributes))
        print("Attributes sent:", attributes)
    def start(self):
        self.client.username_pw_set(ACCESS_TOKEN)
        self.client.on_connect = self.on_connect
        self.client.on_message =  self.on_message
        self.client.connect(THINGSBOARD_HOST, 1883, 60)
        self.send_attributes()
        self.client.loop_start()

 
