/**
 @file read9axis.ino
 @brief This is an Example for the FaBo 9Axis I2C Brick.

   http://fabo.io/202.html

   Released under APACHE LICENSE, VERSION 2.0

   http://www.apache.org/licenses/

 @author FaBo<info@fabo.io>
*/

#include <Wire.h>
#include <FaBo9Axis_MPU9250.h>

FaBo9Axis fabo_9axis;

  float ax,ay,az;
  float gx,gy,gz;
  float mx,my,mz;
  float temp;

long loopTime = 10000;   // microseconds
unsigned long timer = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("RESET");
  Serial.println();

  Serial.println("configuring device.");

  if (fabo_9axis.begin()) {
    Serial.println("configured FaBo 9Axis I2C Brick");
  } else {
    Serial.println("device error");
    while(1);
  }
}

void loop() {

  timeSync(loopTime);

  fabo_9axis.readAccelXYZ(&ax,&ay,&az);
  fabo_9axis.readGyroXYZ(&gx,&gy,&gz);
  fabo_9axis.readMagnetXYZ(&mx,&my,&mz);
  fabo_9axis.readTemperature(&temp);
  
  sendToPC(&gy, &gx, &gz, 
           &ax, &ay, &az,
           &mx, &my, &mz);
}
void sendToPC(float* data1, float* data2, float* data3, 
              float* data4, float* data5, float* data6,
              float* data7, float* data8, float* data9)
{
  byte* byteData1 = (byte*)(data1);
  byte* byteData2 = (byte*)(data2);
  byte* byteData3 = (byte*)(data3);
  byte* byteData4 = (byte*)(data4);
  byte* byteData5 = (byte*)(data5);
  byte* byteData6 = (byte*)(data6);
  byte* byteData7 = (byte*)(data7);
  byte* byteData8 = (byte*)(data8);
  byte* byteData9 = (byte*)(data9);
  byte buf[36] = {byteData1[0], byteData1[1], byteData1[2], byteData1[3],
                 byteData2[0], byteData2[1], byteData2[2], byteData2[3],
                 byteData3[0], byteData3[1], byteData3[2], byteData3[3],
                 byteData4[0], byteData4[1], byteData4[2], byteData4[3],
                 byteData5[0], byteData5[1], byteData5[2], byteData5[3],
                 byteData6[0], byteData6[1], byteData6[2], byteData6[3],
                 byteData7[0], byteData7[1], byteData7[2], byteData7[3],
                 byteData8[0], byteData8[1], byteData8[2], byteData8[3],
                 byteData9[0], byteData9[1], byteData9[2], byteData9[3]};
  Serial.write(buf, 36);
}

void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();
  long timeToDelay = deltaT - (currTime - timer);
  if (timeToDelay > 5000)
  {
    delay(timeToDelay / 1000);
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0)
  {
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative so we start immediately
  }
  timer = currTime + timeToDelay;
}
