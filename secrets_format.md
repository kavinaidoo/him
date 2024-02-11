### Secrets.py 

Create a file called secrets.py and add in your details between the quotes (''). 

- ssid & password refer to the name of your WiFi network and it's password. 
- aio_data_feed_name = Adafruit IO feed name for pressure data
- aio_debug_feed_name = Adafruit IO feed name for error/debugging data (for all him devices)
- pushalert_icon_url & pushalert_url must be [urlencoded](https://en.wikipedia.org/wiki/Percent-encoding). Also, see [PushAlert Docs](https://pushalert.co/dashboard/2/documentation/rest-api).
- pushalert_segment_id - corresponds to the segment created for this specific him device
- device_offset_v and device_error_v refer to the device-specific offset and error values. Offset is tuned so that open to air, the device returns 0kPa. Error is tuned so that voltages below this register as a sensor error.
- device_location_id and device_location_name must match id and name on wpm_sblmnl


````
secrets = {
    'ssid' : '',
    'password' : '',
    'aio_username' : "",
    'aio_key' : '',
    'aio_data_feed_name' : '',
    'aio_debug_feed_name' : '',
    'ntfy_topic': '',
    'pushalert_api_key':'',
    'pushalert_icon_url':'',
    'pushalert_url':'',
    'pushalert_segment_id': 9999,
    'device_offset_v': 0.9999,
    'device_error_v': 0.9999,
    'device_location_id': 0,
    'device_location_name': ''
}     
````

Note: Although the .gitignore file should exclude secrets.py from git, double check that it's not included if you are committing your code to a public repo. The contents should not be shared publicly.