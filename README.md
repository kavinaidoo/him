# Home Input Monitor (HIM)

HIM monitors utility inputs to the home. Designed to work with [wpm_d](https://github.com/kavinaidoo/wpm_d).

---

### Implemented Features
* Water Pressure Monitoring via connected sensor
* Sending data to [Adafruit IO](https://io.adafruit.com/)
* Sending push notifications using [ntfy](https://ntfy.sh/) and [PushAlert](https://pushalert.co/)

---

### Installation Guide
1. Follow "Hardware Setup" and "Software Setup" sections [here](https://kavi.sblmnl.co.za/home-input-monitor-part-1-water-pressure)
2. Download and unzip the latest release from [here](https://github.com/kavinaidoo/him/releases)
3. Install the latest stable release of CircuitPython on your Pico ([Link](https://circuitpython.org/board/raspberry_pi_pico_w/))
4. Copy files from (Step 2) to CIRCUITPY drive on Pico.
5. Use adc_test.py to tune appropriate offset_v and error_v values.
6. Create secrets.py and add in credentials and values from (Step 6) ([Guide](secrets_format.md))
7. Copy secrets.py to CIRCUITPY drive on Pico.
8. Eject CIRCUITPY, disconnect from your computer and connect the Pico W to it's own power supply.
9. Verify in Adafruit IO that you are seeing data sent to the appropriate feed set in (Step 4). By default, sends every 5 minutes.

WARNING: Do not run code.py when connected to your computer. code.py calls microcontroller.reset() when errors occur. This can cause file system corruption (see [here](https://learn.adafruit.com/circuitpython-essentials/circuitpython-resetting#hard-reset-3087083) for details). If you want to run it while connected, comment out all instances of microcontroller.reset() and restart code manually if errors are experienced.

---

### Disclaimer
**Running any software or script from this repo is done entirely at your own risk!**

---

### Credits
This project includes code from:
* Adafruit - Wifi_Mailbox_Notifier code - [Link](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/WiFi_Mailbox_Notifier/mailbox_code/code.py) - MIT License
* Adafruit - adafruit_io library - [Link](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) - MIT License
* Adafruit - adafruit_requests library - [Link](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) - MIT License
* Adafruit - adafruit_minimqtt library - [Link](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) - MIT License

The full licenses for these can be found in [LICENSE.md](LICENSE.md)