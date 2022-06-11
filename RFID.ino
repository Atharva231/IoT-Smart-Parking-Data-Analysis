/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-rfid-nfc
 */

#include <SPI.h>
#include <MFRC522.h>
#include <Arduino.h>
#include <Wire.h>
#define I2C_DEVICE_ADDRESS 0x44
#define SS_PIN 10
#define RST_PIN 9
int n=3,c;
int *slots=new int[n];
int *slots1=new int[n];
String s;
MFRC522 rfid(SS_PIN, RST_PIN);
int f=0;
void sendMsg() {
  if(f==0){
    Wire.write(s.length());
    f=1;
  }
  else{
  Wire.write(s.c_str());
  Serial.println("sent "+s);
  f=0;
  }
}
void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_DEVICE_ADDRESS);
  Wire.onRequest(sendMsg);
  SPI.begin(); // init SPI bus
  rfid.PCD_Init(); // init MFRC522
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  pinMode(8,OUTPUT);
  digitalWrite(8,LOW);
  Serial.println("Tap RFID/NFC Tag on reader");
  for(int i=0;i<n;i++)
  slots[i]=2;
}
void trig(){
  digitalWrite(8,HIGH);
  digitalWrite(8,LOW);
}
void loop() {
  if (rfid.PICC_IsNewCardPresent()) { // new tag is available
    if (rfid.PICC_ReadCardSerial()) { // NUID has been readed
      MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
      //Serial.print("RFID/NFC Tag Type: ");
      //Serial.println(rfid.PICC_GetTypeName(piccType));

      // print NUID in Serial Monitor in the hex format
      Serial.print("UID:");
      s="";
      for (int i = 0; i < rfid.uid.size; i++) {
        //Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
        //Serial.print(rfid.uid.uidByte[i]);
        s+=String(rfid.uid.uidByte[i]);
        s+=(i==rfid.uid.size-1)?"":"-";
      }
      Serial.println(s);
      trig();
      rfid.PICC_HaltA(); // halt PICC
      rfid.PCD_StopCrypto1(); // stop encryption on PCD
    }
  }
  for(int i=0;i<n;i++){
    slots1[i]=!digitalRead(i+2);
  }
  c=0;
  for(int i=0;i<n;i++){
    if(slots[i]^slots1[i]!=0)
    c++;
  }
  s="";
  if(c!=0){
    for(int i=0;i<n;i++){
      slots[i]=slots1[i];
      s+=String(slots[i]);
      if(i!=n-1)
      s+=",";
    }
    Serial.println(s);
    trig();
  }
  if(c!=0)
  delay(500);
}
