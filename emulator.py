from enum import Enum
import paho.mqtt.client as mqtt
import json
import time

from enums import KettleTelemetry, KettleAttributes
from kettle import Kettle

# Replace with your ThingsBoard device access token
THINGSBOARD_HOST = "eu.thingsboard.cloud"
ACCESS_TOKEN = "oS4UCQtsar2rmf8xhOfs"
#
RPC_SUBSCRIPTION_URL = 'v1/devices/me/rpc/request/+'


kettle = Kettle()

def on_set_state(request_id, client,value):
    kettle.power(value)

def on_fill_water(amount):
    kettle.fill_water(amount)
#handle rpc call from platform
def on_rpc_method(request_id,client,method, value):
    if(method == "setState"):
        on_set_state(request_id, client,value)
        return
    if(method == "fillWater"):
        on_fill_water(value)
        return
# Callback when connected
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    # Subscribe to RPC requests
    client.subscribe(RPC_SUBSCRIPTION_URL)    

# Callback when message received
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        if msg.topic.startswith("v1/devices/me/rpc/request/"):
            request_id = msg.topic.split("/")[-1]
            method = data.get("method")
            params = data.get("params")
            on_rpc_method(request_id, client ,method, params)
    except Exception as e:
        print("Error processing message:", e)
        
def send_telemetry(client):
    telemetry = kettle.get_current_telemetry()
    client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
    print("Telemetry sent:", telemetry)
def send_attributes(client):
    attributes = kettle.get_attributes()
    client.publish("v1/devices/me/attributes", json.dumps(attributes))
    print("Attributes sent:", attributes)
def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(ACCESS_TOKEN)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(THINGSBOARD_HOST, 1883, 60)
    send_attributes(client)
    client.loop_start()
    try:
        while True:
            kettle.update_heating()
            send_telemetry(client)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Stopping emulator...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
     main()
 
