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

```python
  ''' 
    @brief  Set temperature and humidity
    @param  mode  The operating mode of the sensor
    @param  iicaddr  The IIC address to be modified
    @return  Whether the device is on or not. return True succeed ;return False failed.
  '''
  def begin(self,mode = self.VL6180X_SINGEL,iicaddr = self.L6180X_IIC_ADDRESS):

  ''' 
    @brief  Obtain ambient light data
    @return Measured ambient light data
  '''
  def get_als_value(self):

  ''' 
    @brief  Obtain range data
    @return Measured range data
  '''
  def get_range_value(self):

  ''' 
    @brief  Gets validation information for range data
    @return Authentication information
  '''
  def get_range_result(self):


```

## Compatibility

* RaspberryPi Version

| Board        | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :-------: | :--------: | :------: | ------- |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python Version

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :-------: | :--------: | :------: | ------- |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## History

- data 2021-02-09
- version V1.0


## Credits

Written by [yangfeng]<feng.yang@dfrobot.com>,2021,(Welcome to our [website](https://www.dfrobot.com/))
