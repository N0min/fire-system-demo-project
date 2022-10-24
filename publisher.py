import paho.mqtt.publish as publish #declare publisher mode in MQTT protocol
import serial
import time
import string
# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm0", 9600)		#declare seial ports "ser" for fire system
ser.write(str.encode('Start\r\n'))
ser1 = serial.Serial("/dev/rfcomm1", 9600)		#declare seial ports "ser1" for motion system
ser1.write(str.encode('Start\r\n'))
oldtemp = 0						#defualt data for data saving mode
oldhumi = 0
while True:
	if ser.in_waiting > 0:				#scaning serial port for fire system
		rawserial = ser.readline()
		cookedserial = rawserial.decode('utf-8').strip('\r\n')
		Temp = cookedserial[32:37]		# get temp data from recieved raw data
		humi = cookedserial[11:16]		# get Humidity data from recieved raw data
		print(Temp)
		
		if float(oldtemp) != float(Temp):	#comparing between old data and recieved data if it's different it will publish
			publish.single("firesys/temp", Temp, hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"}) #publishing command with authentication information
			oldtemp = float(Temp) 		#replace old data to new data
		print(humi)
		if float(oldhumi) != float(humi):
			publish.single("firesys/humi", humi+"%", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
			oldumi = float(humi)
		alarm = cookedserial[45:46]		#get alarm data from raw data
		print(alarm)
		if float(Temp) > 40 and float(humi) <10:		#confir alarm for if temp higher than 40 degree and humi lower than 10%
			publish.single("firesys/alarm/fire","fire", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		if int(alarm) == 1:					#if fire alarm detected pubish the alarm data which is "fire"
			publish.single("firesys/alarm/fire","fire", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		elif int(alarm) == 0:					#turned off fire alarm
			publish.single("firesys/alarm/fire"," ", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})   
	if ser1.in_waiting > 0:				#scan serial port for motion system
		rawserial1 = ser1.readline()
		cookedserial1 = rawserial1.decode('utf-8').strip('\r\n')
		print(cookedserial1)
		alarmMotion = cookedserial1
		if int(alarmMotion) == 1:			#check the recieved data for alarm or not
			publish.single("firesys/alarm/motion", "danger", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		elif int(alarmMotion) == 0:
			publish.single("firesys/alarm/motion", " ", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
