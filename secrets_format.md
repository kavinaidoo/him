### Secrets.py 

Create a file called secrets.py and add in your details between the quotes (''). 

ssid and password refer to the name of your WiFi network and it's password. 

aio = Adafruit IO

````
secrets = {
    'ssid' : '',
    'password' : '',
    'aio_username' : "",
    'aio_key' : '',
    'aio_data_feed_name' : '',
    'ntfy_topic': ''
}     
````

Note: Although the .gitignore file should exclude secrets.py from git, double check that it's not included if you are committing your code to a public repo. The contents should not be shared publicly.