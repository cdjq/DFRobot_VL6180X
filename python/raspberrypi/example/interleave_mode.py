  # -*- coding: utf-8 -*
""" file interleave_mode.py
  # @brief 在交叉测量模式下测量光照数据和距离
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

# 当iic地址被修改后，应当在实例化类时传入更改后的iic地址。iic地址被更改后掉电保存，但是，如果使用了CE引脚进行了传感器重启，iic地址会变回默认地址0x29
# bus ：iic bus
VL6180X = DFRobot_VL6180X(iic_addr= 0x29,bus = 1)

global flag
flag = 0

def int_callback(channel):
  global flag
  if flag == 0:
    flag = 1

GPIO.setwarnings(False)
# Use GPIO port to monitor sensor interrupt
gpio_int = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_int, GPIO.IN)
GPIO.add_event_detect(gpio_int, GPIO.FALLING, callback=int_callback) 

while(VL6180X.begin() == False ):
  print ('Please check that the IIC device is properly connected')

''' mode
   * VL6180X_DIS_INTERRUPT          不开启中断通知功能
   * VL6180X_LOW_INTERRUPT          开启中断通知功能，INT引脚默认输出低电平
   * VL6180X_HIGH_INTERRUPT         开启中断通知功能，INT引脚默认输出高电平
   * 注意：当使用VL6180X_LOW_INTERRUPT模式开启中断通知功能时，请用“RISING”来触发中断，当使用VL6180X_HIGH_INTERRUPT模式开启中断时，请用“FALLING”来触发中断
'''
VL6180X.set_interrupt(mode = VL6180X.VL6180X_HIGH_INTERRUPT)
''' mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
'''
VL6180X.als_config_interrupt(mode = VL6180X.VL6180X_NEW_SAMPLE_READY)
VL6180X.range_config_interrupt(mode = VL6180X.VL6180X_NEW_SAMPLE_READY)
#配置交叉测量周期
VL6180X.als_set_inter_measurement_period(period_ms = 1000)
#开启交叉测量
VL6180X.start_interleaved_mode()

try:
  while True:
    if(flag == 1):
      '''与设置的中断模式相对应
         * No threshold events reported  :                                            0
         * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
         * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
         * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
         * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
      '''      
      if(VL6180X.als_get_interrupt_status() == VL6180X.VL6180X_NEW_SAMPLE_READY):
        # 获取环境光数据
        lux = VL6180X.als_get_measurement()
        # 清除由采集环境光所产生的中断
        VL6180X.clear_als_interrupt()
        print('ALS vlaue : %f lux'%lux) 
        
      if(VL6180X.range_get_interrupt_status() == VL6180X.VL6180X_NEW_SAMPLE_READY):
        # 获取距离数据
        range = VL6180X.range_get_measurement()
        # 获取距离数据判断值
        status = VL6180X.get_range_result()
        # 清除由测距产生的中断
        VL6180X.clear_range_interrupt()
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
        flag = 0
  
except KeyboardInterrupt:
  GPIO.cleanup()    