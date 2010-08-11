import serial, sys, glob

def writeLED(led, status):
	ser = serial.Serial(port="/dev/arduino",baudrate=115200,timeout=3)
	if status == True:	
		ser.write(led.upper()[0])
	elif status == False:
		ser.write(led.lower()[0])
		
	ser.close()

def writeLED_PWM(led, level):
	if level > 255:
		level = 255
	ser = serial.Serial(port="/dev/arduino",baudrate=115200,timeout=3)
	ser.write(led.lower()[0])
	ser.write(chr(level))
	ser.close()
		
def main():
	try:
		if (sys.argv[2] == "on"):
			writeLED_PWM(sys.argv[1], 5)
		elif (sys.argv[2] == "off"):
			writeLED_PWM(sys.argv[1], 0)
		elif (sys.argv[2].isdigit()):
			writeLED_PWM(sys.argv[1], int(sys.argv[2]))
	except:
		print "Error:", sys.exc_info()
		print "Input:", sys.argv
		pass

if __name__ == "__main__":
	main()
