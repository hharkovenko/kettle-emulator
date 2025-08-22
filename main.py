import time
from emulator import Emulator
from kettle import Kettle
import paho.mqtt.client as mqtt

def main():
    kettle = Kettle()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    emulator = Emulator(kettle,client)
    try:
        while True:
            emulator.send_telemetry()
            time.sleep(3)
    except KeyboardInterrupt:
        print("Stopping emulator...")
    finally:
        client.loop_stop()
        client.disconnect()
        kettle.stop()

if __name__ == "__main__":
     main()