#!/usr/bin/python
import sqlite3, time, datetime, os
import recvReading

#settings
loggTime = 5 # nr of minutes between logging to db

def logging():
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	time = datetime.datetime.now().strftime("%H:%M")
	sensorReadings = recvReading.recvReading()
		
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
		if lastLoged != minutesToday:
			if minutesToday % loggTime == 0:
				if logging():
					lastLoged = minutesToday
					os.system("gnuplot daily.plot")
			if minutesToday % 60 == 0:	
					os.system("gnuplot weekly.plot")
			if minutesToday % 300 == 0:		
					os.system("gnuplot monthly.plot")
					os.system("gnuplot monthlyAVG.plot")
		time.sleep(30) # sleep 30 seconds	
			

if __name__ == "__main__":
	main()
