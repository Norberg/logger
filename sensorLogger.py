import sqlite3, time, datetime, os
import readSensor

#settings
loggTime = 5 # nr of minutes between logging to db
sensorLookUp = {"10 DE C6 35 1 8 0 86" : "indoor", \
		"10 87 35 36 1 8 0 5E" : "outdoor", \
		"10 C4 EB 35 1 8 0 6" : "test"}

def logging():
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	time = datetime.datetime.now().strftime("%H:%M")
	sensorReadings = {}
	readings = 0
	while 1:
		try:
			value, id, sensor = readSensor.readSensor()
		except:
			print "not able to get sensor reading:", date, time
			return False # unsuccesfully logged

		try:
			#if sensor allready have been read then we read them all
			if sensorReadings.has_key(sensorLookUp[id]):
				break

			sensorReadings[sensorLookUp[id]] = (sensor, value)
		except:
			print "ID:", id, "not found in sensorLookUp, please add"
		
	try:
		conn = sqlite3.connect("/home/simon/logger/sensors.db")
		c = conn.cursor()
		for name in sensorReadings:
			#date, time, value, sensor, name
			c.execute("insert into sensors values(?, ?, ?, ?, ?)",\
				 [date, time, sensorReadings[name][1], \
				  sensorReadings[name][0], name])

		conn.commit();
		c.close()
	except:
		return False
	print "Successfully written readings to db at:", date, time
	return True # succesfully logged

def main():
	lastLoged = 0
	while 1:
		timetuple = datetime.datetime.now().timetuple()
		minutesToday = timetuple[3] * 60 + timetuple[4]
		#if its time to logg and not allready logged	
		if minutesToday % loggTime == 0 and lastLoged != minutesToday:
			if logging():
				lastLoged = minutesToday
				os.system("gnuplot daily.plot")
				os.system("gnuplot weekly.plot")
				os.system("gnuplot monthly.plot")
				os.system("gnuplot monthlyAVG.plot")
		time.sleep(30) # sleep 30 seconds	
			

if __name__ == "__main__":
	main()
