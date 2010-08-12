#!/usr/bin/python
import json,socket

def recvReading():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(('localhost',7011))
	except:
		print "sensorDispatcher isnt running, please start it first"
		return {}
	data  = s.recv(1000)
	s.close()
	return json.read(data)

def main():
	sensorReadings = recvReading()
	for i, val in sensorReadings.iteritems():
		if val[0] == 'Temp': 
			print i, val[0]+ ':', val[1], "C"
		else:	
			print i, val[0]+ ':', val[1]

	
if __name__ == "__main__":
	main()
