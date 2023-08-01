#include <Wire.h>
#include <VL53L1X.h>
#include "Adafruit_VL53L0X.h"

int EN1 = 5;
int IN1 = 7;
int IN2 = 6;

int EN2 = 10;
int IN3 = 9;
int IN4 = 8;


Adafruit_VL53L0X sensor = Adafruit_VL53L0X();
VL53L1X sensorx;


void TCA9548A(uint8_t bus) //function of TCA9548A
{
  Wire.beginTransmission(0x70);  // TCA9548A address is 0x70
  Wire.write(1 << bus);          // send byte to select bus
  Wire.endTransmission();
}


void Forward( int Speed){
  Serial.println("Forward");
  analogWrite(EN1,Speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  
}


void Reverse( int Speed){
  Serial.println("Reverse");
  analogWrite(EN1,Speed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  
}

void Stop(){
  Serial.println("Stop");
  analogWrite(EN1,0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}


void Steering(char Dir ){
  
  analogWrite(EN2,200);
  
  if (Dir == 'M'){
    digitalWrite(IN3,LOW);
    digitalWrite(IN4,LOW);
  }
  
  if (Dir == 'R'){
    Serial.print("Right");
    digitalWrite(IN3,HIGH);
    digitalWrite(IN4,LOW);
  }

  if (Dir == 'L'){
    Serial.print("Left");
    digitalWrite(IN3,LOW);
    digitalWrite(IN4,HIGH);
  }

}





void setup()
{

    
  Wire.begin();
  delay(100);
  
  Serial.begin(115200);  
  
  delay(500);
  
  Serial.println("Starting I2C Commuincation.");
  
  TCA9548A(3);
  Serial.println("Adafruit VL53L1X test");
  sensorx.setTimeout(500);
  if (!sensorx.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
   }
  sensorx.setDistanceMode(VL53L1X::Long);
  sensorx.setMeasurementTimingBudget(50000);
  sensorx.startContinuous(50);

 TCA9548A(5);
  Serial.println("Adafruit VL53L0X test");
  if ( sensor.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    delay(1000);
  }

  TCA9548A(7);
  Serial.println("Adafruit VL53L0X test");
  if ( sensor.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    delay(1000);
  } 

  pinMode(EN1,OUTPUT);
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(EN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);


}

void loop() {




  VL53L0X_RangingMeasurementData_t right;
  VL53L0X_RangingMeasurementData_t left;


  TCA9548A(3);
  int front = sensorx.read();

  TCA9548A(5);
  sensor.rangingTest(&right, false);  // pass in 'true' to get debug data printout!

  TCA9548A(7);
  sensor.rangingTest(&left, false);  // pass in 'true' to get debug data printout!

  Serial.print(right.RangeMilliMeter);
  Serial.print(" ");
  Serial.print(front);
  Serial.print(" ");
  Serial.println(left.RangeMilliMeter);




  if (front > 1200) {
    Forward(150);
    Steering('M');
  }

  else {


    if (front < 380) {
      if (right.RangeMilliMeter < left.RangeMilliMeter) {
        Steering('R');
        Reverse(200);
      } else if (right.RangeMilliMeter > left.RangeMilliMeter) {
        Steering('L');
        Reverse(200);
      }
    }

    else if (right.RangeMilliMeter < left.RangeMilliMeter) {
      Steering('L');
      Forward(150);
    } else if (right.RangeMilliMeter > left.RangeMilliMeter) {
      Steering('R');
      Forward(150);
    } else {
      Steering('M');
    }
  }
}
