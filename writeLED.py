import serial, sys, socket

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

def writeLEDs(argv):
	print argv
	try:
		color = None
		for arg in argv:
			if color == None:
				color = arg
			elif (arg == "on"):
				writeLED_PWM(color, 5)
				color = None
			elif (arg == "off"):
				writeLED_PWM(color, 0)
				color = None
			elif arg.isdigit():
				writeLED_PWM(color, int(arg))
				color = None
	except:
		print "Error:", sys.exc_info()
		print "Input:", argv

		
def sendLED(argv):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(('localhost',7011))
	except:
		print "sensorDispatcher isnt running, please start it first"
		return
	sep = " "
	output = sep.join(argv)
	s.send(output)
	s.close()

def main():
	sendLED(sys.argv[1:])

if __name__ == "__main__":
	main()
