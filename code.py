# pylance: reportMissingImports=false

# ---- Main Development File for him

# --------------- Copyright

# This code is a modification of https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/WiFi_Mailbox_Notifier/mailbox_code/code.py
# Which contained the following text:

# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# The license (MIT) for the above can be found here: https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/LICENSE

# --------------- Dependency Versions

'''
CircuitPython (MIT) -> adafruit-circuitpython-raspberry_pi_pico_w-en_GB-8.2.9.uf2 - https://circuitpython.org/board/raspberry_pi_pico_w/
'''

# --------------- Import Section

import gc
import time
import ssl
import alarm
import board
import digitalio
import analogio
import wifi
import socketpool
import microcontroller
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP
from secrets import secrets

# --------------- Global Variables

aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]
aio_data_feed_name = secrets["aio_data_feed_name"]
#aio_debug_feed_name = secrets["aio_debug_feed_name"]
ntfy_topic = secrets["ntfy_topic"]
pushalert_api_key = secrets["pushalert_api_key"]
pushalert_icon_url = secrets["pushalert_icon_url"]
pushalert_url = secrets["pushalert_url"]

gc.collect() # running garbage collection

# --------------- Setup and Initialization

# ------ ADC -> Pressure

offset_v = 0.24 # Tune so that open to air it registers 0kpa for water pressure above air pressure

pressure_pin = analogio.AnalogIn(board.A0) # sets up ADC 
pressure_v = round((pressure_pin.value * 3.3)/65536,2) # ADC value to voltage
pressure_kpa = (pressure_v - offset_v)*300 # voltage to pressure

if pressure_kpa < 0: #ensures pressure never goes negative
    pressure_kpa = 0

# ------ Battery Monitoring + Led output

voltage_pin = analogio.AnalogIn(board.VOLTAGE_MONITOR) # Set up battery monitoring.
voltage = (voltage_pin.value / 65536) * 2 * 3.3 # Take the raw voltage pin value, and convert it to voltage.

led = digitalio.DigitalInOut(board.LED) # Set up LED.
led.switch_to_output()

gc.collect() # running garbage collection

# --------------- Function Definitions

def send_io_data(feed_name, value): # Send the data. Requires a feed name and a value to send.
    """
    Send data to Adafruit IO.
    Provide an Adafruit IO feed name, and the value you wish to send.
    """
    feed = io.create_and_get_feed(feed_name)
    return io.send_data(feed["key"], value)

# --------------- Main Program

try: # Connect to WiFi
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
except Exception as error: # any error
    time.sleep(30)
    #removeComment microcontroller.reset() # reboot pico

io = IO_HTTP(aio_username, aio_key, requests) # Initialize an Adafruit IO HTTP API object

print(f"Current pressure_v (voltage in): {pressure_v:.2f}")
print(f"Current pressure_kpa: {pressure_kpa:.2f}")

try: # try to send data to AIO
    led.value = True  # Turn on the LED to indicate data is being sent.
    send_io_data(aio_data_feed_name, f"{pressure_kpa:.2f}")
    time.sleep(30)  # Delay included to avoid data limit throttling on Adafruit IO.
    led.value = False  # Turn off the LED to indicate data sending is complete.
    
except Exception as error: # any error
    time.sleep(30)
    #removeComment microcontroller.reset() # reboot pico

gc.collect() # running garbage collection

# ------ Notifications

#print("----Starting Notification section----")
notification_text = ""
ntfy_headers = {}
pushalert_title = ""
pushalert_message = ""

last_4_full = io.receive_n_data(aio_data_feed_name,4) # pull last 4 values from AIO
last_4_val = [float(x["value"]) for x in last_4_full] # stripping out just the values
last_4_val.reverse() # oldest to newest

if last_4_val[0] == 0 and last_4_val[1] > 0 and last_4_val[2] > 0 and last_4_val[3] > 0:
    # one zero and 3 above zero
    notification_text = "Water is back"
    ntfy_headers = {"Tags": "yellow_circle", "Title": "WPM"} 

if last_4_val[0] <= 100 and last_4_val[1] > 100 and last_4_val[2] > 100 and last_4_val[3] > 100:
    # one below 100 and 3 above 100
    notification_text = "Normal Pressure resumed"
    ntfy_headers = {"Tags": "green_circle", "Title": "WPM"}

if last_4_val[0] >= 100 and last_4_val[1] < 100 and last_4_val[2] < 100 and last_4_val[3] < 100:
    # one above 100 and 3 below 100
    notification_text = "Dropped below Normal Pressure"
    ntfy_headers = {"Tags": "yellow_circle", "Title": "WPM"}

if last_4_val[0] > 0 and last_4_val[1] == 0 and last_4_val[2] == 0 and last_4_val[3] == 0:
    # one above 100 and 3 below 100
    notification_text = "Water Stopped Completely"
    ntfy_headers = {"Tags": "red_circle", "Title": "WPM"}

if notification_text:
    
    if ntfy_topic: # if ntfy_topic has been defined
        try:
            requests.post("https://ntfy.sh/"+ntfy_topic,data=notification_text,headers=ntfy_headers)
        except:
            pass

    if pushalert_api_key: # if pushalert_api_key has been defined
        pushalert_headers = {"Authorization":"api_key="+pushalert_api_key}
        pushalert_data = "title="+pushalert_title+"&message="+pushalert_message+"&icon="+pushalert_icon_url+"&url="+pushalert_url
        try:
            requests.post("https://api.pushalert.co/rest/v1/send",data=pushalert_data,headers=pushalert_headers)
        except:
            pass        

#send_io_data(aio_debug_feed_name,"["+",".join(map(str, last_4_val))+"]"+" - "+notification_text) #sends data to debug-log AIO feed
             
# ------ Preparing for sleep

led.value = False # Turn off LED for deep sleep.

#removeComment time_alarm = alarm.time.TimeAlarm(monotonic_time=(time.monotonic() + 300)) # 300 (5 min) / 60 (1 min) Timer
#removeComment alarm.exit_and_deep_sleep_until_alarms(time_alarm) # Exit and set the alarm to wake up.

