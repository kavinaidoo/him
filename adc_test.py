# pylance: reportMissingImports=false

# ---- adc_test for him

# --------------- Copyright

# Copyright 2024 Kavi Naidoo. Full license text can be found in LICENSE.md

# --------------- Dependency Versions

'''
CircuitPython (MIT) -> adafruit-circuitpython-raspberry_pi_pico_w-en_GB-8.2.9.uf2 - https://circuitpython.org/board/raspberry_pi_pico_w/
'''

# --------------- Import Section

import time
import board
import analogio
from secrets import secrets

offset_v = 0.26 # Tune so that open to air pressure_kpa registers 0kpa
error_v = 0.15 # Voltage below this will signal a sensor failure, does not send reading to AIO, sends a notification to ntfy only

pressure_pin = analogio.AnalogIn(board.A0) # sets up ADC 

while True:
    pressure_v = round((pressure_pin.value * 3.3)/65536,2) # ADC value to voltage
    pressure_kpa = (pressure_v - offset_v)*300 # voltage to pressure

    if pressure_kpa < 0: #ensures pressure never goes negative
        pressure_kpa = 0

    print("[offset_v - "+str(offset_v)+"] [error_v - "+str(error_v)+"] [pressure_v - "+str(pressure_v)+"] [pressure_kpa - "+str(pressure_kpa)+"]")
    #print("error_v - "+str(error_v))
    #print("pressure_v - "+str(pressure_v))
    #print("pressure_kpa - "+str(pressure_kpa))
    time.sleep(1)