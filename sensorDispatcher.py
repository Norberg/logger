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
		try:
			input = conn.recv(1024)
			writeLED.writeLEDs(input.split())
		except socket.error:
			conn.send(json.write(sensorReadings))
			conn.close()

class Dispatcher(threading.Thread):   
	def run(self):  
		while 1:
			conn,addr = s.accept()
			conn.settimeout(1)
			print "connected to:", addr
			Dispatch().run(conn)


class SensorReader(threading.Thread):
	def run(self):
		while 1:
			try:
				value, id, sensor = readSensor.readSensor()
			except:
				print "not able to get sensor reading:"
				continue
			if sensorLookUp.has_key(id):
				sensorReadings[sensorLookUp[id]] = (sensor, value)
			else:		
				print "ID:", id, "not found in sensorLookUp, please add"
Dispatcher().start()
print "dispatcher started"
SensorReader().start()
print "reader started"
