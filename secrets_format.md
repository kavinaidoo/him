### Secrets.py 

Create a file called secrets.py and add in your details between the quotes (''). 

- ssid & password refer to the name of your WiFi network and it's password. 
- aio = Adafruit IO
- pushalert_icon_url & pushalert_url must be [urlencoded](https://en.wikipedia.org/wiki/Percent-encoding). Also, see [PushAlert Docs](https://pushalert.co/dashboard/2/documentation/rest-api).


````
secrets = {
    'ssid' : '',
    'password' : '',
    'aio_username' : "",
    'aio_key' : '',
    'aio_data_feed_name' : '',
    'ntfy_topic': '',
    'pushalert_api_key':'',
    'pushalert_icon_url':'',
    'pushalert_url':''
}     
````

Note: Although the .gitignore file should exclude secrets.py from git, double check that it's not included if you are committing your code to a public repo. The contents should not be shared publicly.