#include <SoftwareSerial.h>
#include "DHT.h"
SoftwareSerial Bluetooth(8,7);//RX and TX
const int buzzer = 0; //buzzer to arduino pin 9
int flame_sensor = 2; //flame sensor pin
int flame_detected;
String buzz = "off";
String fs = "on"
#define DHTPIN 21      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx

void setup(){
 
  pinMode(buzzer, OUTPUT); // Set buzzer - pin 0 as an output
  Serial1.begin(9600); // BT def communication
  pinMode(flame_sensor, INPUT);
}

void loop(){
   if(Serial1.available() > 0){ // Checks whether data is comming from the serial port
   
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
    Serial1.print(f);
    Serial1.print(F("F  Heat index: "));
    Serial1.print(hic);
    Serial1.print(F("C "));
    Serial1.print(hif);
    Serial1.println(F("F"));
   }
   if(fs == "on"){
      flame_detected = digitalRead(flame_sensor);
      if (flame_detected == 1)
      {
        //Serial.println("Flame detected...! take action immediately.");
        digitalWrite(buzzer, HIGH);
        delay(200);
      }
      else
      {
        //Serial.println("No flame detected. stay cool");
        digitalWrite(buzzer, LOW);
      }
    
  delay(1000);
 
      
}
