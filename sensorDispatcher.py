#!/usr/bin/python
import threading, socket, json
import readSensor, writeLED
HOST = ''
PORT = 7011
sensorLookUp = {"10 DE C6 35 1 8 0 86" : "indoor", \
		"10 87 35 36 1 8 0 5E" : "outdoor", \
		"PIN0" : "flower1", \
		"10 C4 EB 35 1 8 0 6" : "test"}

sensorReadings = {}
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
s.listen(5)
class Dispatch(threading.Thread):
	def run(self, conn):
			conn.send(json.dumps(sensorReadings))
			conn.close()

class Dispatcher(threading.Thread):   
	def run(self):  
		while 1:
			conn,addr = s.accept()
			conn.settimeout(1)
			Dispatch().run(conn)


class SensorReader(threading.Thread):
	def run(self):
		while 1:
			try:
				self.readSensors()
			except Exception as e:
				print "Got exception:" + str(e)

	def readSensors(self):
		ser = readSensor.connectArduino()
		while 1:
			value, id, sensor = readSensor.readSensor(ser)
			float(value) # trigger exception if value is not float
			if sensorLookUp.has_key(id):
				sensorReadings[sensorLookUp[id]] = (sensor, value)
			else:		
				print "ID:", id, "not found in sensorLookUp, please add"
Dispatcher().start()
print "dispatcher started"
SensorReader().start()
print "reader started"
