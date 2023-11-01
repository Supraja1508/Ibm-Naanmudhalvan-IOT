import machine
import time
import urequests
import network

# Define your Wi-Fi credentials
wifi_ssid = 'Wokwi-GUEST'
wifi_password = ''

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

# Wait for Wi-Fi connection
while not wifi.isconnected():
    pass

# Define ultrasonic sensor pins
trigger1 = machine.Pin(15, machine.Pin.OUT)
echo1 = machine.Pin(2, machine.Pin.IN)
trigger2 = machine.Pin(4, machine.Pin.OUT)
echo2 = machine.Pin(5, machine.Pin.IN)

# Define traffic light pins
red_light1 = machine.Pin(13, machine.Pin.OUT)
yellow_light1 = machine.Pin(12, machine.Pin.OUT)
green_light1 = machine.Pin(14, machine.Pin.OUT)
red_light2 = machine.Pin(27, machine.Pin.OUT)
yellow_light2 = machine.Pin(26, machine.Pin.OUT)
green_light2 = machine.Pin(25, machine.Pin.OUT)

# Define Firebase Realtime Database URL and secret
firebase_url = 'https://smarttrafficmanagement-1d518-default-rtdb.asia-southeast1.firebasedatabase.app/'
firebase_secret = 'OkE8vnXtjgXk9ceF0jE4A3z3KUK9Ll1sfGO1DK1e'

def ultrasonic_distance(trigger, echo):
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    while echo.value() == 0:
        pulse_start = time.ticks_us()

    while echo.value() == 1:
        pulse_end = time.ticks_us()

    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2
    return distance

def control_traffic_lights(distance1, distance2):
    if distance1 < 50:
        red_light1.off()
        yellow_light1.on()
        green_light1.off()
    elif distance1 < 100:
        red_light1.on()
        yellow_light1.on()
        green_light1.off()
    else:
        red_light1.on()
        yellow_light1.off()
        green_light1.on()

    if distance2 < 50:
        red_light2.off()
        yellow_light2.on()
        green_light2.off()
    elif distance2 < 100:
        red_light2.on()
        yellow_light2.on()
        green_light2.off()
    else:
        red_light2.on()
        yellow_light2.off()
        green_light2.on()

    if distance1 > 100:
        yellow_light1.off()
        red_light1.off()
        green_light1.on()

    if distance2 > 100:
        yellow_light2.off()
        red_light2.off()
        green_light2.on()

    time.sleep(5)  # Keep the yellow light on for 5 seconds

    if distance1 < 50:
        red_light1.off()
        yellow_light1.on()
        green_light1.off()
    else:
        red_light1.on()
        yellow_light1.off()
        green_light1.off()

    if distance2 < 50:
        red_light2.off()
        yellow_light2.on()
        green_light2.off()
    else:
        red_light2.on()
        yellow_light2.off()
        green_light2.off()

def send_data_to_firebase(data):
    url = f'{firebase_url}.json?auth={firebase_secret}'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent to Firebase successfully")
        else:
            print(f"Failed to send data to Firebase. Status code: {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Error sending data to Firebase: {str(e)}")

def print_status_and_distance(distance1, distance2):
    print("Distance 1:", distance1, "Distance 2:", distance2)
    print("Traffic Light 1: Red:", red_light1.value(), "Yellow:", yellow_light1.value(), "Green:", green_light1.value())
    print("Traffic Light 2: Red:", red_light2.value(), "Yellow:", yellow_light2.value(), "Green:", green_light2.value())

while True:
    distance1 = ultrasonic_distance(trigger1, echo1)
    distance2 = ultrasonic_distance(trigger2, echo2)
    control_traffic_lights(distance1, distance2)
    print_status_and_distance(distance1, distance2)

    # Prepare data to send to Firebase
    firebase_data = {
        
        
        "TrafficLightStatus1": {
            "Distance1": distance1,
            "Red": red_light1.value(),
            "Yellow": yellow_light1.value(),
            "Green": green_light1.value()
        },
        "TrafficLightStatus2": {
            "Distance2": distance2,
            "Red": red_light2.value(),
            "Yellow": yellow_light2.value(),
            "Green": green_light2.value()
        }
    }

    # Send data to Firebase
    send_data_to_firebase(firebase_data)

    time.sleep(1)
