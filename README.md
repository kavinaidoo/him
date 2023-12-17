# Home Input Monitor (HIM)

HIM monitors utility inputs to the home.

---

### Implemented Features
* Water Pressure Monitoring
* Sending data to Adafruit IO

---

### Installation Guide
1. Follow "Hardware Setup" and "Software Setup" sections [here](https://kavi.sblmnl.co.za/home-input-monitor-part-1-water-pressure)
2. Download and unzip the latest release from [here](https://github.com/kavinaidoo/him/releases)
3. Install the latest stable release of CircuitPython on your Pico ([Link](https://circuitpython.org/board/raspberry_pi_pico_w/))
4. Create secrets.py and add in credentials ([Link](secrets_format.md))
5. Copy secrets.py and files from (2) to CIRCUITPY.
6. Eject CIRCUITPY, disconnect from your computer and connect the Pico W to it's own power supply.
7. Verify in Adafruit IO that you are seeing data sent to the appropriate feed in (4). By default, sends every 5 minutes.

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

The full licenses for these can be found in [LICENSE.MD](LICENSE.MD)