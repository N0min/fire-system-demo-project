#include <SoftwareSerial.h>
SoftwareSerial Bluetooth(8,7);//RX and TX
int ledRED = 0 ;                //the led for show working status 
int ledGREEN = 2;               // the Led for show detected moviement
int sensor = 21 ;              // Motion sensor pin number
int state = LOW ;               // default status of motion
int val = 0 ;                   //default low value 
int turn;                     // for conrol the detect sensor
String Data = "off";          //default mode for system is off
int alarm = 10;
#define rxPin 7 // Teensy pin 7 <--> HC-05 Tx
#define txPin 8 // Teensy pin 8 <--> HC-05 Rx

void setup ( ) {
  //Bluetooth.begin(9600);
  pinMode ( ledGREEN , OUTPUT ) ;
  pinMode ( ledRED , OUTPUT ) ;
  pinMode ( sensor , INPUT ) ;
 
 Serial1.begin(9600); // BT def communication
 
}

void loop(){
   if(Serial1.available() >0 ){               //scaning serial port and decide system work or not
      Data = Serial1.readString();            
      if( Data == "on"){
        turn = 1;
        Serial.println("system is on");
      }
      else
        if (Data == "off") {
        turn = 0;
        digitalWrite(ledRED, LOW);   // turn LED OFF TURNED OFF SYS
        Serial.println("system is off");
        Serial1.println("0");
       }
     } 
    if ( turn == 1){
      digitalWrite(ledRED, HIGH);   // turn LED ON
      delay(1000);                
      digitalWrite(ledRED, LOW);   // turn LED OFF
      delay(1000);  
      val = digitalRead(sensor);   // read sensor value
        if (val == HIGH) {           // check if the sensor is HIGH
          for( int i = 0; i <= 10; i++){
            digitalWrite(ledGREEN, HIGH);
            delay(100);// delay 100 milliseconds
            digitalWrite(ledGREEN, LOW);
            delay(100); 
            }
             if (state == LOW) {
                //Serial.println("Motion detected!"); 
                  Serial1.println("1");
                  delay(1000);
                    state = HIGH;       // update variable state to HIGH 
              }
           }      
        else {
              delay(20);             // delay 200 milliseconds 
              if (state == HIGH){
                //Serial.println("Motion stopped!");
                Serial1.println("0");
                state = LOW;       // update variable state to LOW
               }
          }
    }      
}
