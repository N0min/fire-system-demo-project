//#include <SoftwareSerial.h>
#include "DHT.h"
//SoftwareSerial Bluetooth(8,7);//RX and TX
const int buzzer = 0; //buzzer to arduino pin 9
int flame_sensor = 2; //flame sensor pin
int flame_detected;
String buzz = "off";
String fs = "on";
int alarm = 0; // default fire alarm mode
#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx
void setup(){
    pinMode(DHTPIN, INPUT);
    dht.begin();
  Serial.begin(9600);
  //Bluetooth.begin(9600);
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 0 as an output
  Serial1.begin(9600); // BT def communication
  pinMode(flame_sensor, INPUT);
}

void loop(){
   if(Serial1.available() > 0){ // Checks whether data is comming from the serial port

   String state=Serial1.readString();
   
    if (state == "on"){
     fs = state;
    Serial.println("fire system is turned on");
    }
     else if(state == "off"){
    fs = state;
      Serial.println("fire system is turned off");
     }
   }
   if(fs == "on"){
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float f = dht.readTemperature(true);
    float hif = dht.computeHeatIndex(f, h);
    float hic = dht.computeHeatIndex(t, h, false);  

    Serial1.print(F(" Humidity: "));
    Serial1.print(h);
    Serial1.print(F("%  Temperature: "));
    Serial1.print(t);
    Serial1.print(F("C "));
    Serial1.print(F("fire: "));
    Serial1.print(alarm);
    Serial1.println(F("F"));
    delay(5000);
    
      flame_detected = digitalRead(flame_sensor);
      if (flame_detected == 1)
      {
        alarm = 1;
        digitalWrite(buzzer, HIGH);     //alarming 
        delay(2000);
        digitalWrite(buzzer, LOW);
        delay(2);
           
      }
      else
      {
        digitalWrite(buzzer, LOW);
        alarm = 0;
      }
    
    delay(1000);
   }
   else if(fs == "off"){
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    float f = dht.readTemperature(true);
    float hif = dht.computeHeatIndex(f, h);
    float hic = dht.computeHeatIndex(t, h, false);  

    Serial1.print(F(" Humidity: "));
    Serial1.print(h);
    Serial1.print(F("%  Temperature: "));
    Serial1.print(t);
    Serial1.print(F("C "));
    Serial1.print(F("fire: "));
    Serial1.print("0");
    Serial1.println(F("F"));
    
    delay(5000);
    
   }
      
}
