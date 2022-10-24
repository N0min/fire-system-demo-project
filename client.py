import paho.mqtt.client as mqtt         #declare mode of client in MQTT protocol 
import serial
import string
import time
fireserial = serial.Serial("/dev/rfcomm0", 9600)  # declare which serial port used 
secureserial = serial.Serial("/dev/rfcomm1", 9600)

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection returned result: " + str(rc) )
    client.subscribe("firesys/control/firesys")
    client.subscribe("firesys/control/security")
def on_message(client, userdata, msg):       # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    print(msg.payload)
    if msg.topic == "firesys/control/firesys":      #check the topic for send data to which port
        fireserial.write(msg.payload)               #send data to fire system's serial port
    elif msg.topic == "firesys/control/security":
        secureserial.write(msg.payload)             #send data to motion system's serial port
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("firesys","1qaz2wsx")            #MQTT authentication method. it needs to some configuration on broker side.  https://www.youtube.com/watch?v=wIiI1yaJ_9s
client.connect("3.25.76.159", 1883, 60)                 #broker IP address port number

client.loop_forever()
