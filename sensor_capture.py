from datetime import datetime
import csv
from Adafruit_BME280 import *

def to_csv(data):
	with open('./data/sensor_data.csv', 'a') as csv_file:
		w = csv.DictWriter(csv_file, data.keys())
		w.writerow(data)

	csv_file.close()

def main():
	sensor = BME280(mode=BME280_OSAMPLE_8)
	while True:
		
		data = {
			"time" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
			"degrees" : '{:.2f}'.format(sensor.read_temperature()),
			"pascals" : '{:.2f}'.format(sensor.read_pressure()),
			"humidity" : '{:.2f}'.format(sensor.read_humidity()),
		}
		
		to_csv(data)
		
		time.sleep(10)

if __name__ == '__main__':
	main()