# Casa Sensori

This is a Raspberry Pi webserver that delievers current temperature, humidity and pressure readings to clients via websockets.  The current iteration reads the senosr anytime someone connects via the websocket.  This is cool but not really what I want.  I want to capture and store sensor data and view that history via a web server.  Therefore, the next version will separate the sensor capture process from the data delivery process.

## Setup

The ```app.py``` file is a **Tornado Websocket Server**.  WHenever a client connects, the server reads the latest time from the ```BME280``` and sends it to all connected devices.  The ```sensor_capture.py``` file is a basic script that captures sensor data and writes it to a csv file in ```./data```.  ```client.py``` is a script that keeps connected to a websocket server.  This is currently not implemented.

>Note: If this doesnt work immediately, check the ```ip address``` of the Rpi and the ```index.html``` websocket address.

## Notes

Best way to capture current time:

```python
'{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
```

Write to a csv file.  The only trick here is that the header is not written.  I've note been able to figure this out yet.

```python
with open('./data/sensor_data.csv', 'a') as csv_file:
	w = csv.DictWriter(csv_file, data.keys())
	w.writerow(data)

csv_file.close()
````