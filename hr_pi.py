import numpy as np
from bluepy.btle import Peripheral, UUID, DefaultDelegate, ADDR_TYPE_RANDOM
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode()))
    
class HRNotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


# UUIDs for the Garmin Forerunner 235 watch
HR_SERVICE_UUID = UUID("0000180d-0000-1000-8000-00805f9b34fb")
HR_MEASUREMENT_CHAR_UUID = UUID("00002a37-0000-1000-8000-00805f9b34fb")

# Set up MQTT client
client = mqtt.Client()
client.connect("172.20.10.3", 1883, 60)
client.subscribe("heart_rate")
client.loop_start()
print("MQTT created")
peripheral = Peripheral()

try:
    # Connect to the watch and discover services and characteristics
    print("Preparing connection..")
    peripheral = Peripheral("D1:91:53:D7:21:65", ADDR_TYPE_RANDOM)
    print("connected")
    hr_service = peripheral.getServiceByUUID(HR_SERVICE_UUID)
    hr_measurement_char = hr_service.getCharacteristics(HR_MEASUREMENT_CHAR_UUID)[0]

    # Enable notifications for heart rate measurements
    peripheral.writeCharacteristic(hr_measurement_char.getHandle() + 1, b"\x01\x00")

    # Set up variables for feature extraction and event detection
    heart_rates = []
    window_size = 10  # seconds
    event_threshold = 120  # bpm

    # Continuously receive and parse heart rate data
    while True:
        if peripheral.waitForNotifications(1.0):
            # Handle heart rate data received
            data = hr_measurement_char.read()
            heart_rate = ord(data[1])
            heart_rates.append(heart_rate)

            # Extract features and detect events
            if len(heart_rates) >= window_size:
                # Compute features
                avg_heart_rate = np.mean(heart_rates)
                max_heart_rate = np.max(heart_rates)
                std_heart_rate = np.std(heart_rates)

                # Detect events
                if max_heart_rate > event_threshold:
                    print("Exercise detected!")
                
                # Publish heart rate data to MQTT broker
                msg = "{{'avg_heart_rate': {}, 'max_heart_rate': {}, 'std_heart_rate': {}}}".format(avg_heart_rate, max_heart_rate, std_heart_rate)
                client.publish("heart_rate", msg)
                
                # Reset heart rate buffer
                heart_rates = []
                
                print("Avg. heart rate: {} bpm".format(avg_heart_rate))
                print("Max. heart rate: {} bpm".format(max_heart_rate))
                print("Std. heart rate: {}".format(std_heart_rate))

except Exception as e:
    print("Error: {}".format(str(e)))
finally:
    peripheral.disconnect()
    client.loop_stop()
