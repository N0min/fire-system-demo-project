import serial
import time
import string
import paho.mqtt.publish as publish
# reading and writing data from and to arduino serially.
# rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))
ser1 = serial.Serial("/dev/rfcomm3", 9600)
ser1.write(str.encode('Start\r\n'))
oldtemp = 0
oldhumi = 0
while True:
	if ser.in_waiting > 0:
		rawserial = ser.readline()
		cookedserial = rawserial.decode('utf-8').strip('\r\n')
		Temp = cookedserial[32:37]
		humi = cookedserial[11:16]
		print(Temp)
		
		if float(oldtemp) != float(Temp):
			publish.single("firesys/temp", Temp, hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
			oldtemp = float(Temp)
		print(humi)
		if float(oldhumi) != float(humi):
			publish.single("firesys/humi", humi+"%", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
			oldumi = float(humi)
		alarm = cookedserial[45:46]
		print(alarm)
		if float(Temp) > 40 and float(humi) <10:
			publish.single("firesys/alarm/fire","fire", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		if int(alarm) == 1:
			publish.single("firesys/alarm/fire","fire", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		elif int(alarm) == 0:
			publish.single("firesys/alarm/fire"," ", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})   
	if ser1.in_waiting > 0:
		rawserial1 = ser1.readline()
		cookedserial1 = rawserial1.decode('utf-8').strip('\r\n')
		print(cookedserial1)
		alarmMotion = cookedserial1
		if int(alarmMotion) == 1:
			publish.single("firesys/alarm/motion", "danger", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
		elif int(alarmMotion) == 0:
			publish.single("firesys/alarm/motion", " ", hostname="3.25.76.159", auth={'username':"firesys", 'password':"1qaz2wsx"})
