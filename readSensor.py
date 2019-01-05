import serial, re

def connectArduino():
	ser = serial.Serial(port="/dev/arduino",baudrate=115200,timeout=3)
	try:
		ser.flushInput() # flush old input before getting new
	except Exception as e:
		print("opening and reading serial port failed" + str(e))
		ser.close()
		raise e
	return ser

def readSensor(ser):
	try:	
		reading = ser.readline().decode("utf-8")
	except Exception as e:
		print("opening and reading serial port failed" + e)
		ser.close()
		raise e
	return parseLine(reading)

def parseLine(input):
	try:
		sensor = re.split(" Sensor: | ", input)[1]
	except e:
		print("exception:" + e);
		print("Incorretly formated:", input)
		return False
		
	if sensor == "Temp":
		try:
			id=re.split("Sensor: | ID: | Temp: |C\r\n", input)[2]
			value=re.split("Sensor: | ID: | Temp: |C\r\n", input)[3]
			value=value.split(" ")[0]
			value=value.strip("C")
		except e:
			print("exception:" + e);
			return False
	elif sensor == "Humidity":
		try:
			id=re.split("Sensor: | ID: | Value: |\r\n",input)[2]
			value=re.split("Sensor: | ID: | Value: |\r\n",input)[3]
		except:
			return False
	elif sensor == "Error":
		print(input);
	else:
		print("Incorretly formated:", input)

	return value, id, sensor 

if __name__ == "__main__":
	ser = connectArduino()
	while 1:
		print(readSensor(ser))
	
	print ("Direct use depricated use recvReading.py instead")

