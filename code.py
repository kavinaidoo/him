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
gc.collect() # running garbage collection
print("* Free memory after importing gc - "+str(gc.mem_free()))


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

gc.collect() # running garbage collection
print("* Free memory after all other imports - "+str(gc.mem_free()))

try: # try statement encapsulates entire code

    # --------------- Global Variables

    aio_username = secrets["aio_username"]
    aio_key = secrets["aio_key"]
    aio_data_feed_name = secrets["aio_data_feed_name"]
    aio_debug_feed_name = secrets["aio_debug_feed_name"]
    ntfy_topic = secrets["ntfy_topic"]
    pushalert_api_key = secrets["pushalert_api_key"]
    pushalert_icon_url = secrets["pushalert_icon_url"]
    pushalert_url = secrets["pushalert_url"]

    gc.collect() # running garbage collection
    print("* Free memory after pulling secrets.py into variables - "+str(gc.mem_free()))

    # --------------- Setup and Initialization

    # ------ ADC -> Pressure

    offset_v = 0.26 # Tune so that open to air it registers 0kpa for water pressure above air pressure
    error_v = 0.15 # Voltage below this will signal an error, does not send to AIO, sends to ntfy

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
    print("* Free memory after getting voltage from ADC - "+str(gc.mem_free()))

    # --------------- Function Definitions

    def send_io_data(feed_name, value): # Send the data. Requires a feed name and a value to send.
        """
        Send data to Adafruit IO.
        Provide an Adafruit IO feed name, and the value you wish to send.
        """
        feed = io.create_and_get_feed(feed_name)
        return io.send_data(feed["key"], value)

    # --------------- Main Program
    print("Trying to Connect to WiFi")
    try: # Connect to WiFi
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        print("- Connected to WiFi")
    except Exception as error: # any error
        print("- WiFi connection failed, resetting in 30s")
        time.sleep(30)
        microcontroller.reset() # reboot pico
    
    gc.collect() # running garbage collection
    print("* Free memory after connecting to WiFi - "+str(gc.mem_free()))
    
    io = IO_HTTP(aio_username, aio_key, requests) # Initialize an Adafruit IO HTTP API object
    
    gc.collect() # running garbage collection
    print("* Free memory after initializing AIO API object - "+str(gc.mem_free()))

    print(f"Current pressure_v (voltage in): {pressure_v:.2f}")
    print(f"Current pressure_kpa: {pressure_kpa:.2f}")
    
    print("Trying to Send Data to AIO")
    try: # try to send data to AIO
        led.value = True  # Turn on the LED to indicate data is being sent.
        if pressure_v >= error_v:     
            send_io_data(aio_data_feed_name, f"{pressure_kpa:.2f}")
        send_io_data(aio_debug_feed_name, f"pressure_v: {pressure_v:.2f}")
        print("- Sending to AIO succeeded, waiting for 30s")
        time.sleep(30)  # Delay included to avoid data limit throttling on Adafruit IO.
        led.value = False  # Turn off the LED to indicate data sending is complete.
        
    except Exception as error: # any error
        print("- Sending to AIO failed, resetting in 30s")
        time.sleep(30)
        microcontroller.reset() # reboot pico
    
    
    offset_v = 0.24 # Tune so that open to air it registers 0kpa for water pressure above air pressure

    del pressure_pin
    del pressure_kpa
    del voltage_pin
    del voltage
    
    gc.collect() # running garbage collection
    print("* Free memory after sending data to AIO - "+str(gc.mem_free()))

    # ------ Notifications

    print("Starting Notification section")
    notification_text = ""
    ntfy_headers = {}
    pushalert_title = ""
    pushalert_message = ""

    last_4_full = io.receive_n_data(aio_data_feed_name,4) # pull last 4 values from AIO
    last_4_val = [float(x["value"]) for x in last_4_full] # stripping out just the values
    last_4_val.reverse() # oldest to newest
    
    del last_4_full
    gc.collect() # running garbage collection
    print("* Free memory after pulling last_4_full - "+str(gc.mem_free()))
    
    print("- Last 4 Values -> "+"["+",".join(map(str, last_4_val))+"]") 
    
    if pressure_v < error_v:
        notification_text = "pressure_v under error_v, sensor error"
        ntfy_headers = {"Tags": "red_circle", "Title": "WPM ERROR"}
    
    if last_4_val[0] == 0 and last_4_val[1] > 0 and last_4_val[2] > 0 and last_4_val[3] > 0:
        # one zero and 3 above zero
        notification_text = "Water is back"
        ntfy_headers = {"Tags": "yellow_circle", "Title": "WPM"}
        pushalert_title = '🟡WPM'

    if last_4_val[0] <= 100 and last_4_val[1] > 100 and last_4_val[2] > 100 and last_4_val[3] > 100:
        # one below 100 and 3 above 100
        notification_text = "Normal Pressure resumed"
        ntfy_headers = {"Tags": "green_circle", "Title": "WPM"}
        pushalert_title = '🟢WPM'

    if last_4_val[0] >= 100 and last_4_val[1] < 100 and last_4_val[2] < 100 and last_4_val[3] < 100:
        # one above 100 and 3 below 100
        notification_text = "Dropped below Normal Pressure"
        ntfy_headers = {"Tags": "yellow_circle", "Title": "WPM"}
        pushalert_title = '🟡WPM'

    if last_4_val[0] > 0 and last_4_val[1] == 0 and last_4_val[2] == 0 and last_4_val[3] == 0:
        # one above 100 and 3 below 100
        notification_text = "Water Stopped Completely"
        ntfy_headers = {"Tags": "red_circle", "Title": "WPM"}
        pushalert_title = '🔴WPM'
    
    del last_4_val
    del io
    del IO_HTTP
    del pool
    del requests
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    
    gc.collect() # running garbage collection
    print("* Free memory after del and recreate pool and requests - "+str(gc.mem_free()))
    
    if notification_text: # if any of the above criteria have been matched
        print("- Notification to be sent -> "+notification_text)

        if ntfy_topic: # if ntfy_topic has been defined
            print("-- Trying to Send to ntfy")
            try:
                requests.post("https://ntfy.sh/"+ntfy_topic,data=notification_text,headers=ntfy_headers)
                print('--- ntfy Sent')
            except Exception as error:
                print('--- ntfy Failed vvv')
                print(error)
                
            del ntfy_topic
            del ntfy_headers
            gc.collect() # running garbage collection
            print("* Free memory after sending to ntfy - "+str(gc.mem_free()))
            
        if pushalert_api_key and pushalert_title: # if pushalert_api_key has been defined
            pushalert_headers = {
                'Authorization': 'api_key='+pushalert_api_key,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            pushalert_data = {
                'title':pushalert_title,
                'message':notification_text,
                'icon':pushalert_icon_url,
                'url':pushalert_url
            }
            print("-- Trying to Send to PushAlert")
            try:
                requests.post("https://api.pushalert.co/rest/v1/send",data=pushalert_data,headers=pushalert_headers)
                print('-- PushAlert Sent')
            except Exception as error:
                print('--- PushAlert Failed vvv')
                print(error) 
            gc.collect() # running garbage collection
            print("* Free memory after sending to PushAlert - "+str(gc.mem_free()))
            
    else:
        print("- No Notification this time")
                    

    #send_io_data(aio_debug_feed_name,"["+",".join(map(str, last_4_val))+"]"+" - "+notification_text) #sends data to debug-log AIO feed
                
    # ------ Preparing for sleep

    led.value = False # Turn off LED for deep sleep.
    print("Going to sleep now, good night :)")
    time_alarm = alarm.time.TimeAlarm(monotonic_time=(time.monotonic() + 300)) # 300 (5 min) / 60 (1 min) Timer
    alarm.exit_and_deep_sleep_until_alarms(time_alarm) # Exit and set the alarm to wake up.

except Exception as error: # any error anywhere in the code
    print("Error in code, resetting in 30s vvv")
    print(error)
    time.sleep(30)
    microcontroller.reset() # reboot pico
