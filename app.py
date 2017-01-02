import os
import time
import json
from tornado import websocket, ioloop, web 
from Adafruit_BME280 import *

cl = []

class IndexHandler(web.RequestHandler):
	'''Handle requests on / '''
	def get(self):
		self.render("index.html")

class WebSocketHandler(websocket.WebSocketHandler):

	# Not sure if this is necessary
	def check_origin(self, origin):
		return True

	def open(self):
		print "Client connected"
		if self not in cl:
			cl.append(self)					

	def on_close(self):
		if self in cl:
			cl.remove(self)

	def on_message(self, message):
		print "Client received message: %s" %(message)
		sensor = BME280(mode=BME280_OSAMPLE_8)

		data = {'temperature' : sensor.read_temperature(),
				'pressure': sensor.read_pressure(),
				'humidity': sensor.read_humidity()}
		print data
		data = json.dumps(data)
		for c in cl:
			c.write_message(data)

class ApiHandler(web.RequestHandler):
	"""Send messages to all clients

	<url>:5000/api?temp=X&hum=Y
	"""
	@web.asynchronous
	def get(self, *args):
		self.finish()

		# parse URL for parameters (not sure why this is in GET request and not POST)
		data = {"temp": self.get_argument("temp"), 
				"hum": self.get_argument("hum"),
				}

		data = json.dumps(data)
		for c in cl:
			c.write_message(data)

	@web.asynchronous
	def post(self):
		pass    	


def main():
	settings = {
		"template_path": os.path.join(os.path.dirname(__file__), "templates"),
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
		"debug" : True
	}
	app = web.Application(
		[
			(r'/', IndexHandler),
			(r'/ws', WebSocketHandler),
			(r'/api', ApiHandler),
		], **settings
	)

	port = int(os.environ.get("PORT", 5000))
	print "Listening on port: %s"%(port)
	app.listen(port)
	ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()