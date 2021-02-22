/*!
 * @file DFRobot_VL6180X.cpp
 * @brief Implementation of DFRobot_VL6180X class
 * @copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @SKU SEN0427
 * @licence The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version V1.0
 * @date 2021-02-08
 * @url  https://github.com/DFRobot/DFRobot_VL6180X
 */
#include <DFRobot_VL6180X.h>

DFRobot_VL6180X::DFRobot_VL6180X(uint8_t addr,TwoWire *pWire):
_pWire(pWire)
{
  _deviceAddr = addr;
  _modeGpio1Reg.reversed=0;
  _modeGpio1Reg.select = 0;
  _modeGpio1Reg.polarity = 0;
  _modeGpio1Reg.reservedBit6_7 = 0;
  
  _configIntGPIOReg.rangeIntMode=0;
  _configIntGPIOReg.alsIntMode=0;
  _configIntGPIOReg.reservedBit6_7=0;

  _clearIntReg.intClearSig = 0;
  _clearIntReg.reserved = 0;

  _rangeStartReg.startstop = 0;
  _rangeStartReg.select = 0;
  _rangeStartReg.reserved = 0;

  _ALSStartReg.startstop = 0;
  _ALSStartReg.select = 0;
  _ALSStartReg.reserved = 0;

  _analogueGainReg.gain = 6;
  _analogueGainReg.gain = 8;
  
  _gain = 1.0;
  _atime =100;
  _continuousRangeMode = false;
  _continuousALSMode = false;
}

bool DFRobot_VL6180X::begin(uint8_t mode,uint8_t iicaddr)
{
  _pWire->begin();
  setIICAddr(iicaddr);
  if((getDeviceID()!=VL6180X_ID)){
    return false;
  }
  if(read(VL6180X_SYSTEM_FRESH_OUT_OF_RESET,1)){
    init();
  }
  setMode(mode);
  write8byte(VL6180X_SYSTEM_FRESH_OUT_OF_RESET,0);
  return true;
}

void DFRobot_VL6180X::init()
{
  write8byte(0x0207, 0x01);
  write8byte(0x0208, 0x01);
  write8byte(0x0096, 0x00);
  write8byte(0x0097, 0xfd);
  write8byte(0x00e3, 0x00);
  write8byte(0x00e4, 0x04);
  write8byte(0x00e5, 0x02);
  write8byte(0x00e6, 0x01);
  write8byte(0x00e7, 0x03);
  write8byte(0x00f5, 0x02);
  write8byte(0x00d9, 0x05);
  write8byte(0x00db, 0xce);
  write8byte(0x00dc, 0x03);
  write8byte(0x00dd, 0xf8);
  write8byte(0x009f, 0x00);
  write8byte(0x00a3, 0x3c);
  write8byte(0x00b7, 0x00);
  write8byte(0x00bb, 0x3c);
  write8byte(0x00b2, 0x09);
  write8byte(0x00ca, 0x09);
  write8byte(0x0198, 0x01);
  write8byte(0x01b0, 0x17);
  write8byte(0x01ad, 0x00);
  write8byte(0x00ff, 0x05);
  write8byte(0x0100, 0x05);
  write8byte(0x0199, 0x05);
  write8byte(0x01a6, 0x1b);
  write8byte(0x01ac, 0x3e);
  write8byte(0x01a7, 0x1f);
  write8byte(0x0030, 0x00);/*
  // Recommended : Public registers - See data sheet for more detail
  write8byte(0x0011, 0x10); // Enables polling for ‘New Sample ready’ 
   // when measurement completes
  write8byte(0x010a, 0x30); // Set the averaging sample period
   // (compromise between lower noise and 
   // increased execution time)
  write8byte(0x003f, 0x46); // Sets the light and dark gain (upper 
   // nibble). Dark gain should not be 
   // changed.
  write8byte(0x0031, 0xFF); // sets the # of range measurements after 
   // which auto calibration of system is
   // performed 
  write8byte(0x0041, 0x63); // Set ALS integration time to 100ms
  
  write8byte(0x002e, 0x01); // perform a single temperature calibration
   // of the ranging sensor 
  //Optional: Public registers - See data sheet for more detail
  write8byte(0x001b, 0x09); // Set default ranging inter-measurement 
   // period to 100ms
  write8byte(0x003e, 0x31); // Set default ALS inter-measurement period 
   // to 500ms
  write8byte(0x0014, 0x24); // Configures interrupt on ‘New Sample 
   // Ready threshold event’*/
  write8byte(VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD,0x09);
  write8byte(VL6180X_SYSRANGE_VHV_REPEAT_RATE,0xFF);
  write8byte(VL6180X_SYSRANGE_VHV_RECALIBRATE,0x01);
  
  write8byte(VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME,0x31);
  write8byte(VL6180X_SYSRANGE_RANGE_CHECK_ENABLES,0x11);
  write16byte(VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE,125);
  setRangeThresholdValue(0,0xFF);

  write8byte(VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x09);
  write8byte(VL6180X_SYSALS_INTEGRATION_PERIOD,0x63);
  setALSThresholdValue(0,0xFFFF);
  
  write8byte(VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD,0x30);
  setALSGain(VL6180X_ALS_GAIN_1);
  write8byte(VL6180X_FIRMWARE_RESULT_SCALER,0x01);
  
  write8byte(VL6180X_SYSTEM_MODE_GPIO0,0x00);
  _modeGpio1Reg.select = 8;
  _modeGpio1Reg.polarity = 1;
  write8byte(VL6180X_SYSTEM_MODE_GPIO1,*((uint8_t*)(&_modeGpio1Reg)));
  
  _configIntGPIOReg.rangeIntMode = 4;
  _configIntGPIOReg.alsIntMode = 4;
  write8byte(VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO,*((uint8_t*)(&_configIntGPIOReg)));
  write8byte(VL6180X_SYSRANGE_START,0);
  write8byte(VL6180X_SYSALS_START,0);
  write8byte(VL6180X_INTERLEAVED_MODE_ENABLE,0x00);
}

void DFRobot_VL6180X::setMode(uint8_t mode)
{
  write8byte(VL6180X_INTERLEAVED_MODE_ENABLE,0x00);
  delay(1);
  switch(mode){
  case VL6180X_SINGEL:
    _continuousRangeMode = false;
    _continuousALSMode = false;
    break;
  case VL6180X_CONTINUOUS_RANGE:
    _continuousRangeMode = true;
    _continuousALSMode = false;
    _rangeStartReg.startstop = 1;
    _rangeStartReg.select = 1;
    write8byte(VL6180X_SYSRANGE_START,*((uint8_t*)(&_rangeStartReg)));
    break;
  case VL6180X_CONTINUOUS_ALS:
    _continuousRangeMode = false;
    _continuousALSMode = true;
    _ALSStartReg.startstop = 1;
    _ALSStartReg.select = 1;
    write8byte(VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x14);
    write8byte(VL6180X_SYSALS_INTEGRATION_PERIOD,0x63);
    write8byte(VL6180X_SYSALS_START,*((uint8_t*)(&_ALSStartReg)));
    break;
  case VL6180X_INTERLEAVED_MODE:
    _continuousRangeMode = true;
    _continuousALSMode = true;
    write8byte(VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME,0x1E);
    write8byte(VL6180X_SYSALS_INTEGRATION_PERIOD,0x63);
    write8byte(VL6180X_SYSALS_INTERMEASUREMENT_PERIOD,0x0F);
    write16byte(VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE,0xCC);
    write8byte(VL6180X_INTERLEAVED_MODE_ENABLE,0x01);
    _ALSStartReg.startstop = 1;
    _ALSStartReg.select = 1;
    write8byte(VL6180X_SYSALS_START,*((uint8_t*)(&_ALSStartReg)));
    break;
  }
}

uint8_t DFRobot_VL6180X::getDeviceID()
{
  return (uint8_t)read(VL6180X_IDENTIFICATION_MODEL_ID,1);
}

float DFRobot_VL6180X::getALSValue()
{
  _ALSStartReg.startstop = 1;
  if(_continuousALSMode){
    _ALSStartReg.select = 1;
  }
  write8byte(VL6180X_SYSALS_START,*((uint8_t*)(&_ALSStartReg)));
  float value = read(VL6180X_RESULT_ALS_VAL,2);
  _clearIntReg.intClearSig = 2;
  write8byte(VL6180X_SYSTEM_INTERRUPT_CLEAR,*((uint8_t*)(&_clearIntReg)));
  value  = (0.32*100*value)/(_gain*_atime);
  return value;
}

uint8_t DFRobot_VL6180X::getALSResult()
{
  return read(VL6180X_RESULT_ALS_STATUS,1)>>4;
}

bool DFRobot_VL6180X::setALSGain(uint8_t gain)
{
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,1);
  if(gain>7){
    write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0);
    return false;
  }else{
    _analogueGainReg.gain = gain;
    switch(gain){
    case VL6180X_ALS_GAIN_20:
       _gain = 20;
       break;
    case VL6180X_ALS_GAIN_10:
       _gain = 10;
       break;
    case VL6180X_ALS_GAIN_5:
       _gain = 5.0;
       break;
    case VL6180X_ALS_GAIN_2_5:
       _gain = 2.5;
       break;
    case VL6180X_ALS_GAIN_1_67:
       _gain = 1.67;
       break;
    case VL6180X_ALS_GAIN_1_25:
       _gain = 1.25;
       break;
    case VL6180X_ALS_GAIN_1:
       _gain = 1.0;
       break;
    case VL6180X_ALS_GAIN_40:
       _gain = 40;
       break;
  }
    write8byte(VL6180X_SYSALS_ANALOGUE_GAIN,*((uint8_t*)(&_analogueGainReg)));
  }
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,1);
  return true;
}

void DFRobot_VL6180X::setALSThresholdValue(uint16_t thresholdL,uint16_t thresholdH)
{
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,1);
  write16byte(VL6180X_SYSALS_THRESH_LOW,thresholdL);
  write16byte(VL6180X_SYSALS_THRESH_HIGH,thresholdH);
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0);
}

uint8_t DFRobot_VL6180X::getRangeVlaue()
{
  _rangeStartReg.startstop = 1;
  if(_continuousRangeMode){
    _rangeStartReg.select = 1;
  }
  write8byte(VL6180X_SYSRANGE_START,*((uint8_t*)(&_rangeStartReg)));
  uint8_t value = read(VL6180X_RESULT_RANGE_VAL,1);
  _clearIntReg.intClearSig = 1;
  write8byte(VL6180X_SYSTEM_INTERRUPT_CLEAR,0x07);
  return value;
}

uint8_t DFRobot_VL6180X::getRangeResult()
{
  return read(VL6180X_RESULT_RANGE_STATUS,1)>>4;
}

void DFRobot_VL6180X::setRangeThresholdValue(uint8_t thresholdL,uint8_t thresholdH)
{
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,1);
  write8byte(VL6180X_SYSRANGE_THRESH_LOW,thresholdL);
  write8byte(VL6180X_SYSRANGE_THRESH_HIGH,thresholdH);
  write8byte(VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD,0);
}
void DFRobot_VL6180X::setIICAddr(uint8_t addr)
{
  write8byte(VL6180X_I2C_SLAVE_DEVICE_ADDRESS,addr);
  _deviceAddr = addr;
}

void DFRobot_VL6180X:: write8byte(uint16_t regAddr,uint8_t value)
{
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(regAddr>>8);
  _pWire->write(regAddr);
  _pWire->write(value);
  _pWire->endTransmission();
}

void DFRobot_VL6180X:: write16byte(uint16_t regAddr,uint16_t value)
{
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(regAddr>>8);
  _pWire->write(regAddr);
  _pWire->write(value>>8);
  _pWire->write(value);
  _pWire->endTransmission();
}

uint16_t DFRobot_VL6180X:: read(uint16_t regAddr,uint8_t readNum)
{
  uint16_t value=0;
  uint8_t  a ,b;
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(regAddr>>8);
  _pWire->write(regAddr&0xFF);
  _pWire->endTransmission();
  _pWire->requestFrom(_deviceAddr, readNum);
  if(readNum==1){
    value = _pWire->read();
  }else if(readNum == 2){
    b = _pWire->read();
    a = _pWire->read();
    value = (b<<8)|a;
  }
  return value;
}