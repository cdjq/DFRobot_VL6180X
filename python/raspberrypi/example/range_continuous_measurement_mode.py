  # -*- coding: utf-8 -*
""" file range_continuous_measurement_mode.py
  # @brief 本传感器工作可工作在四种中断模式下，分别是低于下阈值触发中断模式、高于上阈值触发中断模式、低于下阈值或者高于上阈值触发中断模式以及新样本值采集完成触发中断模式
  # @n 本示例介绍了在连续测距模式下的四种中断
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

global flag
flag = 0

def int_callback(channel):
  global flag
  if flag == 0:
    flag = 1

# CE与传感器的shutdown引脚相连，CE引脚编号采用BCM编码格式
while(VL6180X.begin(CE = 9) == False ):
  print ('Please check that the IIC device is properly connected')

''' 配置INT的中断通知功能
   * mode
   * VL6180X_DIS_INTERRUPT          不开启中断通知功能
   * VL6180X_LOW_INTERRUPT          开启中断通知功能，INT引脚默认输出低电平
   * VL6180X_HIGH_INTERRUPT         开启中断通知功能，INT引脚默认输出高电平
   * 注意：当使用VL6180X_LOW_INTERRUPT模式开启中断通知功能时，请用“RISING”来触发中断，当使用VL6180X_HIGH_INTERRUPT模式开启中断时，请用“FALLING”来触发中断
'''
VL6180X.set_interrupt(mode = VL6180X.VL6180X_HIGH_INTERRUPT)
''' 配置测距的中断模式
   * mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
'''
VL6180X.range_config_interrupt(mode = VL6180X.VL6180X_NEW_SAMPLE_READY)
# 配置测距周期
VL6180X.range_set_inter_measurement_period(period_ms = 1000)
# 配置阈值
VL6180X.set_range_threshold_value(threshold_l = 30,threshold_h = 100)

GPIO.setwarnings(False)
# Use GPIO port to monitor sensor interrupt
gpio_int = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_int, GPIO.IN)
GPIO.add_event_detect(gpio_int, GPIO.FALLING , callback=int_callback) 
VL6180X.range_start_continuous_mode()

try:
  while True:
    if(flag == 1):
      flag = 0
      '''
         * No threshold events reported  :                                            0
         * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
         * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
         * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
         * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
      '''
      if(VL6180X.range_get_interrupt_status() == VL6180X.VL6180X_NEW_SAMPLE_READY):
        # 获取距离数据
        range = VL6180X.range_get_measurement()
        # 获取距离数据的判断结果
        status = VL6180X.get_range_result()
        # 清除测距产生的中断
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

except KeyboardInterrupt:
  GPIO.cleanup()    