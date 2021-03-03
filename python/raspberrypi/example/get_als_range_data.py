# -*- coding: utf-8 -*
""" file get_als_range_data.py
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
#bus iic bus
#addr 默认设置0x29,在VL6180X.begin(mode,iicaddr)中支持修改iic addr,如果修改了其他值，下次使用时应该在实例化DFRobot_VL6180X类的时侯传入修改的iic addr，否则将无法进行IIC通讯
VL6180X = DFRobot_VL6180X(bus = 1,addr=0x29)

while(VL6180X.begin(iicaddr = 0x29) == False ):
  print ('Please check that the IIC device is properly connected')

while True:
  lux = VL6180X.get_als_value()
  print('ALS vlaue : %f lux'%lux)
  range = VL6180X.get_range_value()
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