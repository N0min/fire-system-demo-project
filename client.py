import paho.mqtt.client as mqtt
import serial
import string
import time
fireserial = serial.Serial("/dev/rfcomm0", 9600)
secureserial = serial.Serial("/dev/rfcomm3", 9600)

def on_connect(client, userdata, flags, rc): # func for making connection
    print("Connected to MQTT")
    print("Connection returned result: " + str(rc) )
    client.subscribe("firesys/control/firesys")
    client.subscribe("firesys/control/security")
def on_message(client, userdata, msg):       # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    print(msg.payload)
    if msg.topic == "firesys/control/firesys":
        fireserial.write(msg.payload)
    elif msg.topic == "firesys/control/security":
        secureserial.write(msg.payload)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("firesys","1qaz2wsx")
client.connect("3.25.76.159", 1883, 60)

client.loop_forever()
