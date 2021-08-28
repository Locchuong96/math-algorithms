#include "AccelGyro.h"

#define LSM303D_I2C_ADDRESS B0011101
#define LSM303D_CTRL1       0x20
#define LSM303D_CTRL5       0x24
#define LSM303D_OUT_X_L_A   0x28
#define LSM303D_OUT_X_L_M   0x08

#define L3GD20H_I2C_ADDRESS B1101011
#define L3GD20H_CTRL1       0x20
#define L3GD20H_CTRL4       0x23
#define L3GD20H_OUT_X_L     0x28

AccelGyro::AccelGyro() {}

AccelGyro::~AccelGyro() {}

void
AccelGyro::setAccelSettings(uint8_t accelDataRate, uint8_t antiAliasFilterBW, uint8_t accelScale)
{
    Wire.begin();
    uint8_t ctrl1 = (accelDataRate << 4) | B111;    // Set the accelDataRate and enable XYZ accel
    uint8_t ctrl2 = (antiAliasFilterBW << 6) | (accelScale << 3);
    Wire.beginTransmission(LSM303D_I2C_ADDRESS);
    Wire.write(LSM303D_CTRL1 | _BV(7));                      // Set register pointer to LSM303D_CTRL1; multibyte write/read requires 1 at the MSB
    Wire.write(ctrl1);
    Wire.write(ctrl2);
    Wire.endTransmission();
}

void
AccelGyro::getAccel(Point* data)
{
    Wire.beginTransmission(LSM303D_I2C_ADDRESS);
    Wire.write(LSM303D_OUT_X_L_A | _BV(7));                     // Set register pointer to LSM303D_OUT_X_L_A; multibyte write/read requires 1 at the MSB
    Wire.endTransmission();
    Wire.requestFrom(LSM303D_I2C_ADDRESS, 6, true);             // Request 6 byte of data from register LSM303D_OUT_X_L_A
    uint8_t lowBit = Wire.read();
    data->X = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Y = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Z = (Wire.read() << 8) | lowBit;
}

void
AccelGyro::setMagSettings(uint8_t resolution, uint8_t magDataRate, uint8_t magScale, uint8_t sensorMode)
{
    Wire.begin();
    uint8_t ctrl1 = (resolution << 5) | (magDataRate << 2);    // Set the resolution and data rate
    uint8_t ctrl2 = magScale << 5;
    uint8_t ctrl3 = sensorMode;
    Wire.beginTransmission(LSM303D_I2C_ADDRESS);
    Wire.write(LSM303D_CTRL5 | _BV(7));                      // Set register pointer to LSM303D_CTRL1; multibyte write/read requires 1 at the MSB
    Wire.write(ctrl1);
    Wire.write(ctrl2);
    Wire.write(ctrl3);
    Wire.endTransmission();
}

void
AccelGyro::getMag(Point* data)
{
    Wire.beginTransmission(LSM303D_I2C_ADDRESS);
    Wire.write(LSM303D_OUT_X_L_M | _BV(7));                     // Set register pointer to LSM303D_OUT_X_L_A; multibyte write/read requires 1 at the MSB
    Wire.endTransmission();
    Wire.requestFrom(LSM303D_I2C_ADDRESS, 6, true);             // Request 6 byte of data from register LSM303D_OUT_X_L_A
    uint8_t lowBit = Wire.read();
    data->X = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Y = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Z = (Wire.read() << 8) | lowBit;
}

void
AccelGyro::setGyroSettings(uint8_t gyroDataRate, uint8_t bwSelection, uint8_t gyroScale)
{
    Wire.begin();
    uint8_t ctrl1 = (gyroDataRate << 6) | (bwSelection << 4) | _BV(3) | B111;    // Set the gyroDataRate and bwSelection and enable XYZ gyro
    Wire.beginTransmission(L3GD20H_I2C_ADDRESS);
    Wire.write(L3GD20H_CTRL1);                      // Set register pointer to LSM303D_CTRL1;
    Wire.write(ctrl1);
    Wire.endTransmission();

    uint8_t ctrl4 = (gyroScale << 4);
    Wire.beginTransmission(L3GD20H_I2C_ADDRESS);
    Wire.write(L3GD20H_CTRL4);                      // Set register pointer to LSM303D_CTRL4;
    Wire.write(ctrl4);
    Wire.endTransmission();
}

void
AccelGyro::getAngVel(Point* data)
{
    Wire.beginTransmission(L3GD20H_I2C_ADDRESS);
    Wire.write(L3GD20H_OUT_X_L | _BV(7));                     // Set register pointer to LSM303D_OUT_X_L_A; multibyte write/read requires 1 at the MSB
    Wire.endTransmission();
    Wire.requestFrom(L3GD20H_I2C_ADDRESS, 6, true);             // Request 6 byte of data from register LSM303D_OUT_X_L_A
    uint8_t lowBit = Wire.read();
    data->X = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Y = (Wire.read() << 8) | lowBit;
    lowBit = Wire.read();
    data->Z = (Wire.read() << 8) | lowBit;
}
