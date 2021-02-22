# -*- coding: utf-8 -*
""" file DFRobot_VL6180X.py
  # DFRobot_VL6180X Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [yangfeng]<feng.yang@dfrobot.com> 
  @version  V1.0
  @date  2021-02-09
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_VL6180X
"""
import smbus
import time

class DFRobot_VL6180X:
  VL6180X_IIC_ADDRESS                          = 0x29
  VL6180X_IDENTIFICATION_MODEL_ID             = 0x000
  VL6180X_SYSTEM_MODE_GPIO0                   = 0X010
  VL6180X_SYSTEM_MODE_GPIO1                   = 0X011
  VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO        = 0x014
  VL6180X_SYSTEM_INTERRUPT_CLEAR              = 0x015
  VL6180X_SYSTEM_FRESH_OUT_OF_RESET           = 0x016
  VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD       = 0x017
  VL6180X_SYSRANGE_START                      = 0x018
  VL6180X_SYSRANGE_THRESH_HIGH                = 0x019
  VL6180X_SYSRANGE_THRESH_LOW                 = 0x01A
  VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD    = 0x01B
  VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME       = 0x01C
  VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE = 0x022
  VL6180X_SYSRANGE_MAX_AMBIENT_LEVEL_MULT     = 0x02C
  VL6180X_SYSRANGE_RANGE_CHECK_ENABLES        = 0x02D
  VL6180X_SYSRANGE_VHV_RECALIBRATE            = 0x02E
  VL6180X_SYSRANGE_VHV_REPEAT_RATE            = 0x031
  VL6180X_SYSALS_START                        = 0x038
  VL6180X_SYSALS_THRESH_HIGH                  = 0x03A
  VL6180X_SYSALS_THRESH_LOW                   = 0x03C
  VL6180X_SYSALS_INTERMEASUREMENT_PERIOD      = 0x03E
  VL6180X_SYSALS_ANALOGUE_GAIN                = 0x03F
  VL6180X_SYSALS_INTEGRATION_PERIOD           = 0x040
  VL6180X_RESULT_RANGE_STATUS                 = 0x04D
  VL6180X_RESULT_ALS_STATUS                   = 0x04E
  VL6180X_RESULT_INTERRUPT_STATUS_GPIO        = 0x04F
  VL6180X_RESULT_ALS_VAL                      = 0x050
  VL6180X_RESULT_RANGE_VAL                    = 0x062
  VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD     = 0x10A
  VL6180X_FIRMWARE_RESULT_SCALER              = 0x120
  VL6180X_I2C_SLAVE_DEVICE_ADDRESS            = 0x212
  VL6180X_INTERLEAVED_MODE_ENABLE             = 0x2A3
  
  VL6180X_ID                                  = 0xB4
  VL6180X_ALS_GAIN_20                         = 0
  VL6180X_ALS_GAIN_10                         = 1
  VL6180X_ALS_GAIN_5                          = 2
  VL6180X_ALS_GAIN_2_5                        = 3
  VL6180X_ALS_GAIN_1_67                       = 4
  VL6180X_ALS_GAIN_1_25                       = 5
  VL6180X_ALS_GAIN_1                          = 6
  VL6180X_ALS_GAIN_40                         = 7
  
  VL6180X_NO_ERR                              = 0x00
  VL6180X_ALS_OVERFLOW_ERR                    = 0x01
  VL6180X_ALS_UNDERFLOW_ERR                   = 0x02
  VL6180X_NO_ERR                              = 0x00
  VL6180X_EARLY_CONV_ERR                      = 0x06
  VL6180X_MAX_CONV_ERR                        = 0x07
  VL6180X_IGNORE_ERR                          = 0x08
  VL6180X_MAX_S_N_ERR                         = 0x0B
  VL6180X_RAW_Range_UNDERFLOW_ERR             = 0x0C
  VL6180X_RAW_Range_OVERFLOW_ERR              = 0x0D
  VL6180X_Range_UNDERFLOW_ERR                 = 0x0E
  VL6180X_Range_OVERFLOW_ERR                  = 0x0F
  
  VL6180X_SINGEL                              = 0x00
  VL6180X_CONTINUOUS_RANGE                    = 0x01
  VL6180X_CONTINUOUS_ALS                      = 0x02
  VL6180X_INTERLEAVED_MODE                    = 0x03

  ''' 
    @brief  Module init
    @param  bus  Set to IICBus
  '''
  def __init__(self,bus = 1,addr = VL6180X_IIC_ADDRESS):
    self.__i2cbus = smbus.SMBus(bus)
    self.__i2c_addr = addr
    self.__gain = 1.0
    self.__atime =100
    self.__continuousRangeMode = False
    self.__continuousALSMode = False

  ''' 
    @brief  Set temperature and humidity
    @param  mode  The operating mode of the sensor
    @param  iicaddr  The IIC address to be modified
    @return  Whether the device is on or not. return True succeed ;return False failed.
  '''
  def begin(self,iicaddr = VL6180X_IIC_ADDRESS):
    self.__set_iic_addr(iicaddr)
    device_id = self.__get_device_id()
    if device_id != self.VL6180X_ID:
      return False
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_FRESH_OUT_OF_RESET>>8, [self.VL6180X_SYSTEM_FRESH_OUT_OF_RESET])
    reset = self.__i2cbus.read_byte(self.__i2c_addr)
    if(reset):
      self.__init()
    self.__set_mode(self.VL6180X_INTERLEAVED_MODE)
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_FRESH_OUT_OF_RESET>>8, [self.VL6180X_SYSTEM_FRESH_OUT_OF_RESET,0])
    return True 

  ''' 
    @brief  Obtain ambient light data
    @return Measured ambient light data
  '''
  def get_als_value(self):
    if(self.__continuousALSMode):
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_START>>8, [self.VL6180X_SYSALS_START,0x03])
    else:
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_START>>8, [self.VL6180X_SYSALS_START,0x03])
    value = 0
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_RESULT_ALS_VAL>>8, [self.VL6180X_RESULT_ALS_VAL])
    value = self.__i2cbus.read_byte(self.__i2c_addr)
    value = value<<8                        
    value |= (self.__i2cbus.read_byte(self.__i2c_addr)&0xFF)
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_INTERRUPT_CLEAR>>8, [self.VL6180X_SYSTEM_INTERRUPT_CLEAR,0x02])
    value  = ((0.32*100*value)/(self.__gain*self.__atime))
    return value

  ''' 
    @brief  Obtain range data
    @return Measured range data
  '''
  def get_range_value(self):
    if(self.__continuousRangeMode):
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_START>>8, [self.VL6180X_SYSRANGE_START,0x03])
    else:
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_START>>8, [self.VL6180X_SYSRANGE_START,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_RESULT_RANGE_VAL>>8, [self.VL6180X_RESULT_RANGE_VAL])
    value = self.__i2cbus.read_byte(self.__i2c_addr)
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_INTERRUPT_CLEAR>>8, [self.VL6180X_SYSTEM_INTERRUPT_CLEAR,0x01])
    return value

  ''' 
    @brief  Gets validation information for range data
    @return Authentication information
  '''
  def get_range_result(self):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_RESULT_RANGE_STATUS>>8, [self.VL6180X_RESULT_RANGE_STATUS])
    result = self.__i2cbus.read_byte(self.__i2c_addr)>>4
    return result

  ''' 
    @brief  set IIC addr
    @param  addr  The IIC address to be modified
  '''
  def __set_iic_addr(self,addr):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_I2C_SLAVE_DEVICE_ADDRESS>>8, [self.VL6180X_I2C_SLAVE_DEVICE_ADDRESS,addr])
    self.__i2c_addr = addr

  ''' 
    @brief  Initialize the sensor configuration
  '''
  def __init(self):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x02, [0x07,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x02, [0x08,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0x96,0x00])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0x97,0xfd])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xe3,0x00])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xe4,0x04])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xe5,0x02])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xe6,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xe7,0x03])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xf5,0x02])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xd9,0x05])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xdb,0xce])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xdc,0x03])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xdd,0xf8])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0x9f,0x00])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xa3,0x3c])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xb7,0x00])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xbb,0x3c])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xb2,0x09])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xca,0x09])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0x98,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0xb0,0x17])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0xad,0x00])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0xff,0x05])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0x00,0x05])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0x99,0x05])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0xa6,0x1b])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0xac,0x3e])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x01, [0xa7,0x1f])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,0x00, [0x30,0x00])
    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD>>8, [self.VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD,0x09])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_VHV_REPEAT_RATE>>8, [self.VL6180X_SYSRANGE_VHV_REPEAT_RATE,0xFF])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_VHV_RECALIBRATE>>8, [self.VL6180X_SYSRANGE_VHV_RECALIBRATE,0x01])    
    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME>>8, [self.VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME,0x31])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_RANGE_CHECK_ENABLES>>8, [self.VL6180X_SYSRANGE_RANGE_CHECK_ENABLES,0x11])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE>>8, [self.VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE,0x00,0x7D])    
    self.__set_range_threshold_value(0,0xFF)
    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD>>8, [self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x09])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTEGRATION_PERIOD>>8, [self.VL6180X_SYSALS_INTEGRATION_PERIOD,0x63])    
    self.__set_als_threshold_value(0,0xFFFF)
    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD>>8, [self.VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD,0x30])    
    self.__set_als_gain(self.VL6180X_ALS_GAIN_1)
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_FIRMWARE_RESULT_SCALER>>8, [self.VL6180X_FIRMWARE_RESULT_SCALER,0x01])    
    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_MODE_GPIO0>>8, [self.VL6180X_SYSTEM_MODE_GPIO0,0x20])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_MODE_GPIO1>>8, [self.VL6180X_SYSTEM_MODE_GPIO1,0x10])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO>>8, [self.VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO,0x24])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_START>>8, [self.VL6180X_SYSRANGE_START,0x00])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_START>>8, [self.VL6180X_SYSALS_START,0x00])    
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_INTERLEAVED_MODE_ENABLE>>8, [self.VL6180X_INTERLEAVED_MODE_ENABLE,0x00])    

  ''' 
    @brief  set IIC addr
    @param  mode  The operating mode of the sensor
  '''
  def __set_mode(self,mode):
    if(mode == self.VL6180X_SINGEL):
      self.__continuousRangeMode = False
      self.__continuousALSMode = False      
    elif(mode == self.VL6180X_CONTINUOUS_RANGE):
      self.__continuousRangeMode = True
      self.__continuousALSMode = False
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_START>>8, [self.VL6180X_SYSRANGE_START,0x03]) 
    elif(mode == self.VL6180X_CONTINUOUS_ALS):
      self.__continuousRangeMode = False
      self.__continuousALSMode = True
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD>>8, [self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x14])    
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTEGRATION_PERIOD>>8, [self.VL6180X_SYSALS_INTEGRATION_PERIOD,0x63]) 
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_START>>8, [self.VL6180X_SYSALS_START,0x03]) 
    elif(mode == self.VL6180X_INTERLEAVED_MODE):
      self.__continuousRangeMode = True
      self.__continuousALSMode = True
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME>>8, [self.VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME,0x1E])    
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE>>8, [self.VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE,0x00,0xCC])
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD>>8, [self.VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x0F])    
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_INTEGRATION_PERIOD>>8, [self.VL6180X_SYSALS_INTEGRATION_PERIOD,0x63]) 
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_INTERLEAVED_MODE_ENABLE>>8, [self.VL6180X_INTERLEAVED_MODE_ENABLE,0x01]) 
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_START>>8, [self.VL6180X_SYSALS_START,0x03])

  ''' 
    @brief  Set Range Threshold Value
    @param  thresholdL :Lower Threshold
    @param  thresholdH :Upper threshold
  '''
  def __set_range_threshold_value(self,threshold_l,threshold_h):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_THRESH_LOW>>8, [self.VL6180X_SYSRANGE_THRESH_LOW,threshold_l])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSRANGE_THRESH_HIGH>>8, [self.VL6180X_SYSRANGE_THRESH_HIGH,threshold_h])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x00])

  ''' 
    @brief  Set ALS Threshold Value
    @param  thresholdL :Lower Threshold
    @param  thresholdH :Upper threshold
  '''
  def __set_als_threshold_value(self,threshold_l,threshold_h):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x01])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_THRESH_LOW>>8, [self.VL6180X_SYSALS_THRESH_LOW,threshold_l>>8,threshold_l])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_THRESH_HIGH>>8, [self.VL6180X_SYSALS_THRESH_HIGH,threshold_h>>8,threshold_h])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x00])

  ''' 
    @brief  Set the ALS gain 
    @param  gain  the value of gain(range:0-7).
    @return true :Set up the success, false :Setup failed
  '''
  def __set_als_gain(self,gain):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x01])
    if(gain>7):
      self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x00])
      return False
    if(gain == self.VL6180X_ALS_GAIN_20):
      _gain = 20
    elif(gain == self.VL6180X_ALS_GAIN_10):
      _gain = 10
    elif(gain == self.VL6180X_ALS_GAIN_5):
      _gain = 5.0
    elif(gain == self.VL6180X_ALS_GAIN_2_5):
      _gain = 2.5
    elif(gain == self.VL6180X_ALS_GAIN_1_67):
      _gain = 1.67
    elif(gain == self.VL6180X_ALS_GAIN_1_25):
      _gain = 1.25
    elif(gain == self.VL6180X_ALS_GAIN_1):
      _gain = 1.0
    elif(gain == self.VL6180X_ALS_GAIN_40):
      _gain = 40
    gain =gain | 0x40
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSALS_ANALOGUE_GAIN>>8, [self.VL6180X_SYSALS_ANALOGUE_GAIN,gain])
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD>>8, [self.VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0x00])
    return True

  ''' 
    @brief  get the identifier of sensor
    @return Authentication information
  '''
  def __get_device_id(self):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_IDENTIFICATION_MODEL_ID>>8, [self.VL6180X_IDENTIFICATION_MODEL_ID])
    id = self.__i2cbus.read_byte(self.__i2c_addr)
    return id

  ''' 
    @brief  Gets validation information for ALS data
    @return Authentication information
  '''
  def __get_als_result(self):
    self.__i2cbus.write_i2c_block_data(self.__i2c_addr,self.VL6180X_RESULT_ALS_STATUS>>8, [self.VL6180X_RESULT_ALS_STATUS])
    result = self.__i2cbus.read_byte(self.__i2c_addr)>>4
    return result


