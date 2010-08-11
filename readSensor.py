import serial, re
ser=serial.Serial(port="/dev/arduino",baudrate=115200,timeout=3)
def readSensor():
	try:	
		ser.open()
		ser.flushInput() # flush old input before getting new
		input = ser.readline()
		ser.close()
	except:
		print "opening and reading serial port failed"
		ser.close()
	try:
		sensor = re.split(" Sensor: | ", input)[1]
	except:
		print "Incorretly formated:", input
		return False
		
	if sensor == "Temp":
		try:
			id=re.split("Sensor: | ID: | Temp: |C\r\n", input)[2]
			value=re.split("Sensor: | ID: | Temp: |C\r\n", input)[3]
		except:
			return False
	elif sensor == "Humidity":
		try:
			id=re.split("Sensor: | ID: | Value: |\r\n",input)[2]
			value=re.split("Sensor: | ID: | Value: |\r\n",input)[3]
		except:
			return False
	elif sensor == "Error":
		print input
	else:
		print "Incorretly formated:", input

	return value, id, sensor 

def main():
	import json,socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost',7011))
	data  = s.recv(1000)
	s.close()
	sensorReadings = json.read(data)
	for i, val in sensorReadings.iteritems():
		if val[0] == 'Temp': 
			print i, val[0]+ ':', val[1], "C"
		else:	
			print i, val[0]+ ':', val[1]

	
if __name__ == "__main__":
	main()
