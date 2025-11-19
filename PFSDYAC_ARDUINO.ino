#include <Wire.h>

const int NUNCHUK_ADDR = 0x52;
const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Wire.begin(); 
  nunchuk_init();
}

void loop() {

  Wire.beginTransmission(NUNCHUK_ADDR);
  Wire.write(0x00);
  if (Wire.endTransmission() != 0) {
    nunchuk_init();
    return;
  }
  delay(10);
  

  Wire.requestFrom(NUNCHUK_ADDR, 6);
  if (Wire.available() >= 6) {

    int joy_x = Wire.read(); 
    int joy_y = Wire.read();  
    int acc_x = Wire.read();  
    int acc_y = Wire.read();  
    int acc_z = Wire.read();  
    int btn   = Wire.read();  


    Serial.print(joy_x); Serial.print(","); 
    Serial.print(joy_y); Serial.print(","); 
    Serial.print(acc_x); Serial.print(","); 
    Serial.print(acc_y); Serial.print(","); 
    Serial.println(acc_z);                  


    if (joy_y > 200) digitalWrite(LED_PIN, HIGH);
    else digitalWrite(LED_PIN, LOW);
  }
  delay(50); 
}

void nunchuk_init() {
  Wire.beginTransmission(NUNCHUK_ADDR);
  Wire.write(0xF0); Wire.write(0x55);
  Wire.endTransmission();
  delay(10);
  Wire.beginTransmission(NUNCHUK_ADDR);
  Wire.write(0xFB); Wire.write(0x00);
  Wire.endTransmission();
  delay(10);
}