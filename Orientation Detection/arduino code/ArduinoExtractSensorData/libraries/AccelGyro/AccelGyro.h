#ifndef ACCELGYRO_h
#define ACCELGYRO_h

#include "Arduino.h"
#include "Wire.h"

typedef struct {
    int X;
    int Y;
    int Z;
} Point;

class AccelGyro
{
  public:
    AccelGyro();
    ~AccelGyro();

    void
    setAccelSettings(uint8_t accelDataRate, uint8_t antiAliasFilterBW, uint8_t accelScale);

    void
    setMagSettings(uint8_t resolution, uint8_t magDataRate, uint8_t magScale, uint8_t sensorMode);

    void
    setGyroSettings(uint8_t gyroDataRate, uint8_t bwSelection, uint8_t gyroScale);

    void
    getAccel(Point* data);

    void
    getMag(Point* data);

    void
    getAngVel(Point* data);
};

#endif
