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

if __name__ == "__main__":
	print "Direct use depricated use recvReading.py instead"

