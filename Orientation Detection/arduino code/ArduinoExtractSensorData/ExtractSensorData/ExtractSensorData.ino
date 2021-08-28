#include <AccelGyro.h>

unsigned long timer = 0;
Point accelData = {0};
Point magData = {0};
Point gyroData = {0};
long loopTime = 10000;   // microseconds
AccelGyro sensor;

void setup() {
  Serial.begin(115200);
  Wire.setClock(400000);
  uint8_t accelDataRate = B1000;    // 400Hz
  uint8_t antiAliasFilterBW = B11;  // 50Hz
  uint8_t accelScale = 0;           // 2g
  sensor.setAccelSettings(accelDataRate, antiAliasFilterBW, accelScale);

  uint8_t resolution = B11;   // High resolution
  uint8_t magDataRate = B101; // 100Hz
  uint8_t magScale = B00;     // 2gauss
  uint8_t sensorMode = B00;   // Continuous-conversion mode
  sensor.setMagSettings(resolution, magDataRate, magScale, sensorMode);
  
  uint8_t gyroDataRate = B10;     // 400Hz
  uint8_t bwSelection = B01;      // Cutoff freq at 25Hz
  uint8_t gyroScale = B0;          // 245dps
  sensor.setGyroSettings(gyroDataRate, bwSelection, gyroScale);
  timer = micros();
}

void loop() {
  timeSync(loopTime);
  sensor.getAngVel(&gyroData);  // Gyro Data
  sensor.getAccel(&accelData);  // Accelerometer Data
  sensor.getMag(&magData);      // Magnetometer Data
  
  sendToPC(&gyroData.X, &gyroData.Y, &gyroData.Z, 
           &accelData.X, &accelData.Y, &accelData.Z,
           &magData.X, &magData.Y, &magData.Z);
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

void sendToPC(double* data1, double* data2, double* data3, 
              double* data4, double* data5, double* data6,
              double* data7, double* data8, double* data9)
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

void sendToPC(int* data1, int* data2, int* data3, 
              int* data4, int* data5, int* data6, 
              int* data7, int* data8, int* data9)
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
  byte buf[18] = {byteData1[0], byteData1[1],
                 byteData2[0], byteData2[1],
                 byteData3[0], byteData3[1],
                 byteData4[0], byteData4[1],
                 byteData5[0], byteData5[1],
                 byteData6[0], byteData6[1],
                 byteData7[0], byteData7[1],
                 byteData8[0], byteData8[1],
                 byteData9[0], byteData9[1]};
  Serial.write(buf, 18);
}
