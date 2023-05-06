Team members: Dylan Gatua


Instructions on how to compile/ execute code:
  Install Mosquitto MQTT broker on the Raspberry Pi:
      
      $   sudo apt-get update
      $   sudo apt-get install mosquitto

  Install the Mosquitto Python client on the Raspberry Pi:
  
      $   pip install paho-mqtt

  Pair the Garmin Forerunner 235 watch with the Raspberry Pi using the Bluetooth settings:
          
          Turn on Bluetooth on the Raspberry Pi by running:  
          $   sudo systemctl enable bluetooth
          $   sudo systemctl start bluetooth

          Put the Garmin Forerunner 235 into pairing mode by turning on Bluetooth

          On the Raspberry Pi, open the Bluetooth settings:
          $   bluetoothctl

          Turn on the Bluetooth adapter:
          $   power on

          Start scanning for nearby Bluetooth devices.
          $   scan on

          Wait for the Raspberry Pi to detect the Garmin Forerunner 235. The device name will be Forerunner 235.
          *Take note of the MAC Address

          Pair the Raspberry Pi with the Garmin Forerunner 235:
          $   pair <device-address> 
          *Replace <device-address> with the address of the Garmin Forerunner 235, which can be found in the output of the scan on command.

          Follow the prompts on the Raspberry Pi and the Garmin Forerunner 235 to complete the pairing process.

  Modify the Python script to include the correct MAC address of the watch and the IP address of the Raspberry Pi.

  Run the Python script on the Raspberry Pi using the following command:
  
    $ python3 hr_pi.py

  Open a new terminal window and subscribe to the "heart_rate" topic to receive heart rate data:
      
      $ mosquitto_sub -h <ip_address_of_Raspberry_Pi> -t heart_rate
  *Replace <ip_address_of_Raspberry_Pi> with the IP Address of the Raspberry Pi

  The heart rate data should be displayed in the terminal window where the Mosquitto subscriber is running.
  
List of any external libraries that were used:
numpy, bluepy, paho.mqtt, mosquitto, bluetooth, bluez
