#!/usr/bin/python
import threading, socket, json
import paho.mqtt.publish as publish

import readSensor

MQTT_HOST = "localhost"
sensorLookUp = {"10 DE C6 35 1 8 0 86" : "indoor", \
		"10 CD AA A 2 8 0 82" : "outdoor", \
		"PIN0" : "flower1", \
		"10 C4 EB 35 1 8 0 6" : "test"}


class SensorReader(threading.Thread):
	def run(self):
		while 1:
			try:
				self.readSensors()
			except Exception as e:
				print ("Got exception:", e)

	def readSensors(self):
		ser = readSensor.connectArduino()
		while 1:
			temperature, identity, sensor = readSensor.readSensor(ser)
			float(temperature) # trigger exception if temperature is not float
			if identity in sensorLookUp:
				sensorName = sensorLookUp[identity];
				publish.single("/sensors/temperature/" + sensorName,temperature, hostname=MQTT_HOST);
				print("published " + sensorName + " with " + temperature)
			else:		
				print ("ID:", identity, "not found in sensorLookUp, please add")


def main():
	SensorReader().start()
	print ("reader started")

if __name__ == "__main__":
	main();
