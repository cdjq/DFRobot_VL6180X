# DFRobot_VL6180X

The VL6180X is the latest product based on ST’s patented FlightSense™technology. This is a ground-breaking technology allowing absolute distance to be measured independent of target reflectance. Instead of estimating the distance by measuring the amount of light reflected back from the object (which is significantly influenced by color and surface), the VL6180X precisely measures the time the light takes to travel to the nearest object and reflect back to the sensor (Time-of-Flight).

## 产品链接（https://www.dfrobot.com/）
    SKU：SEN0427

## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)
<snippet>
<content>

## Summary
Measures absolute range from 0 to above 10 cm

Measurement of ambient light data

## Installation

To use this library, download the library file first, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.

## Methods

```C++
  /**
   * @brief  Initialization function
   * @param  mode  The operating mode of the sensor
   * @param  iicaddr  The IIC address to be modified
   * @return Whether the device is on or not. return true succeed ;return false failed.
   */
  bool begin(uint8_t mode = VL6180X_SINGEL,uint8_t iicaddr = VL6180X_IIC_ADDRESS);

  /**
   * @brief  Obtain ambient light data
   * @return Measured ambient light data
   */
  float getALSValue();

  /**
   * @brief  Obtain range data
   * @return Measured range data
   */
  uint8_t getRangeVlaue();

  /**
   * @brief  Gets validation information for range data
   * @return Authentication information
   */
  uint8_t getRangeResult();


```

## Compatibility

| MCU                | Work Well | Work Wrong | Untested | Remarks |
| ------------------ | :-------: | :--------: | :------: | ------- |
| Arduino uno        |     √     |            |          |         |
| FireBeetle esp32   |     √     |            |          |         |
| FireBeetle esp8266 |     √     |            |          |         |
| FireBeetle m0      |           |     √      |          |         |
| Leonardo           |     √     |            |          |         |
| Microbit           |     √     |            |          |         |
| Arduino MEGA2560   |     √     |            |          |         |


## History


## History

- data 2021-02-09
- version V1.0


## Credits

Written by [yangfeng]<feng.yang@dfrobot.com>,2021,(Welcome to our [website](https://www.dfrobot.com/))
