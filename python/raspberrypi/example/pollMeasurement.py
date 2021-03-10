# -*- coding: utf-8 -*
""" file pollMeasurement.py
  # @brief Measures absolute range from 0 to above 10 cm 
  # @n Measurement of ambient light data
  # @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  # @licence     The MIT License (MIT)
  # @author      [yangfeng]<feng.yang@dfrobot.com> 
  # @version  V1.0
  # @date  2021-02-09
  # @get from https://www.dfrobot.com
  # @url https://github.com/DFRobot/DFRobot_VL6180X
"""
import sys
sys.path.append('../')
from DFRobot_VL6180X import DFRobot_VL6180X
import time
import RPi.GPIO as GPIO
#bus iic bus
VL6180X = DFRobot_VL6180X(bus = 1)

# CE与传感器的shutdown引脚相连，CE引脚编号采用BCM编码格式
while(VL6180X.begin(CE = 12) == False ):
  print ('Please check that the IIC device is properly connected')

'''
  * 20   times gain: VL6180X_ALS_GAIN_20                       
  * 10   times gain: VL6180X_ALS_GAIN_10                       
  * 5    times gain: VL6180X_ALS_GAIN_5                        
  * 2.5  times gain: VL6180X_ALS_GAIN_2_5                      
  * 1.57 times gain: VL6180X_ALS_GAIN_1_67                     
  * 1.27 times gain: VL6180X_ALS_GAIN_1_25                     
  * 1    times gain: VL6180X_ALS_GAIN_1                        
  * 40   times gain: VL6180X_ALS_GAIN_40                       
'''
VL6180X.set_als_gain(VL6180X.VL6180X_ALS_GAIN_1)
VL6180X.set_iic_addr(0x39)

while True:
  lux = VL6180X.als_poll_measurement()
  print('ALS vlaue : %f lux'%lux)
  time.sleep(1)

  range = VL6180X.range_poll_measurement()
  status = VL6180X.get_range_result()
  
  if(status ==VL6180X.VL6180X_NO_ERR ):
    print('Range vlaue : %d mm'%range)
  elif(status ==VL6180X.VL6180X_EARLY_CONV_ERR ):
    print('RANGE ERR: ECE check failed !')
  elif(status ==VL6180X.VL6180X_MAX_CONV_ERR ):
    print('RANGE ERR: System did not converge before the specified max!')
  elif(status ==VL6180X.VL6180X_IGNORE_ERR ):
    print('RANGE ERR: Ignore threshold check failed !')
  elif(status ==VL6180X.VL6180X_MAX_S_N_ERR ):
    print('RANGE ERR: Measurement invalidated!')
  elif(status ==VL6180X.VL6180X_RAW_Range_UNDERFLOW_ERR ):
    print('RANGE ERR: RESULT_RANGE_RAW < 0!')
  elif(status ==VL6180X.VL6180X_RAW_Range_OVERFLOW_ERR ):
    print('RESULT_RANGE_RAW is out of range !')
  elif(status ==VL6180X.VL6180X_Range_UNDERFLOW_ERR ):
    print('RANGE ERR: RESULT__RANGE_VAL < 0 !')
  elif(status ==VL6180X.VL6180X_Range_OVERFLOW_ERR ):
    print('RANGE ERR: RESULT__RANGE_VAL is out of range !')
  else: 
    print('RANGE ERR: Systerm err !')
 
  time.sleep(1)