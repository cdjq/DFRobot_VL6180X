  # -*- coding: utf-8 -*
""" file range_continuous_measurement_mode.py
  # @brief The sensor can operate in four interrupt modes: 1. Trigger interrupt when below the L-threshold(lower threshold)
  # @n                                                     2. Trigger interrupt when above the U-threshold(upper threshold)
  # @n                                                     3. Trigger interrupt when below the L-threshold or above the U-threshold
  # @n                                                     4. Trigger interrupt after the new sample value acquisition
  # @n This example introduces four interrupts under continuous range measurement mode
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

# When the IIC address is changed, the revised address should be passed in when instantiating class. And the changed I2C address will be saved after power-down.
# But if the sensor is restarted by using the CE pin, the IIC address will be back to the default address 0x29
# bus：iic bus
VL6180X = DFRobot_VL6180X(iic_addr= 0x29,bus = 1)

global flag
flag = 0

def int_callback(channel):
  global flag
  if flag == 0:
    flag = 1

while(VL6180X.begin() == False ):
  print ('Please check that the IIC device is properly connected')

'''Set the interrupt notification function of INT pin
   * mode
   * VL6180X_DIS_INTERRUPT          Not enable interrupt notification function
   * VL6180X_LOW_INTERRUPT          Enable interrupt notification function, by default the INT pin outputs low level
   * VL6180X_HIGH_INTERRUPT         Enable interrupt notification function, by default the INT pin outputs high level
   * Note: When using the VL6180X_LOW_INTERRUPT mode to enable the interrupt, please use "RISING" to trigger it. 
   *       When using the VL6180X_HIGH_INTERRUPT mode to enable the interrupt, please use "FALLING" to trigger it.
'''
VL6180X.set_interrupt(mode = VL6180X.VL6180X_HIGH_INTERRUPT)
''' Configure the interrupt mode for ranging
   * mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
'''
VL6180X.range_config_interrupt(mode = VL6180X.VL6180X_NEW_SAMPLE_READY)
# Set range measurement period

VL6180X.range_set_inter_measurement_period(period_ms = 1000)
# Set threshold
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
        # Get range
        range = VL6180X.range_get_measurement()
        # Get judgement of range measurement
        status = VL6180X.get_range_result()
        # Clear interrupts generated by measuring distance
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
