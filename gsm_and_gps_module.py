#include <TinyGPS.h>
#include <SoftwareSerial.h>
#include <Wire.h>
 
SoftwareSerial Gsm(9, 10);          // RX, TX pins for GSM module
char phone_no[] = "phone no here";  // Put Your phone number
TinyGPS gps;
int buttonState;
unsigned long buttonPressTime;
bool isSMSsent = false;
 
void setup() {
  Serial.begin(9600);
  Gsm.begin(9600);
 
  Gsm.print("AT+CMGF=1\r");
  delay(100);
 
  Gsm.print("AT+CNMI=2,2,0,0,0\r");
  delay(100);
 
  pinMode(5, INPUT_PULLUP);
}
 
void loop() {
  bool newData = false;
  unsigned long chars;
  unsigned short sentences, failed;
 
  for (unsigned long start = millis(); millis() - start < 1000;) {
    while (Serial.available()) {
      char c = Serial.read();
      Serial.print(c);  // Output GPS data to the Serial Monitor
      if (gps.encode(c))
        newData = true;  // Check if there is new GPS data
    }
  }
 
  buttonState = digitalRead(5);
 
  if (buttonState == LOW) {  // Button is pressed
    if (!isSMSsent) {
      buttonPressTime = millis();
 
      float flat, flon;
      unsigned long age;
      gps.f_get_position(&flat, &flon, &age);
 
      Gsm.print("AT+CMGF=1\r");
      delay(400);
      Gsm.print("AT+CMGS=\"");
      Gsm.print(phone_no);
      Gsm.println("\"");
      Gsm.println("Alert I Need help...");
      Gsm.print("http://maps.google.com/maps?q=loc:");
      Gsm.print(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
      Gsm.print(",");
      Gsm.print(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
      delay(200);
      Gsm.println((char)26);
      delay(200);
      Serial.println("SMS Sent");
      isSMSsent = true;
    }
  } else {
    isSMSsent = false;
    delay(10);
  }
 
  Serial.println(failed);
}
