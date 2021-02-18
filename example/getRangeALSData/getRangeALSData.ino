/*!
 * @file getRangeALSData.ino
 * @brief Measures absolute range from 0 to above 10 cm 
 * @n Measurement of ambient light data
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2021-02-08
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_VL6180X
 */
#include <DFRobot_VL6180X.h>
#include <Wire.h>
//iicaddr 默认设置为0x29,在VL6180X.begin(mode,iicaddr)中支持修改iic addr，默认修改是为0x29，如果修改了其他值，下次使用时应该在实例化DFRobot_VL6180X类的时侯传入修改的iic addr，否则将无法进行IIC通讯
//DFRobot_VL6180X VL6180X(/*addr*/0x29,/*pWire*/&Wire);
DFRobot_VL6180X VL6180X;
void setup() {
  Serial.begin(115200);

  /** param：mode  默认是 VL6180X_SINGEL
        VL6180X_SINGEL                    0x00           A single measurement of ALS and range
        VL6180X_CONTINUOUS_RANGE          0x01           Continuous measuring range
        VL6180X_CONTINUOUS_ALS            0x02           Continuous measuring ALS
        VL6180X_INTERLEAVED_MODE          0x03           Continuous cross measurement of ALS and range
      param： iicaddr 默认是 0x29
  */
  //while(!(VL6180X.begin(/*mode*/VL6180X_SINGEL,/*iicaddr*/0x29))){
  //  Serial.println("Please check that the IIC device is properly connected!");
  //  delay(1000);
  //}
  while(!(VL6180X.begin())){
    Serial.println("Please check that the IIC device is properly connected!");
    delay(1000);
  }
}

void loop() {
  float lux = VL6180X.getALSValue();
  String str ="ALS: "+String(lux)+" lux";
  Serial.println(str);
  uint8_t range = VL6180X.getRangeVlaue();
  uint8_t status = VL6180X.getRangeResult();
  String str1 = "Range: "+String(range) + " mm"; 
  switch(status){
  case VL6180X_NO_ERR:
    Serial.println(str1);
    break;
  case VL6180X_EARLY_CONV_ERR:
    Serial.println("RANGE ERR: ECE check failed !");
    break;
  case VL6180X_MAX_CONV_ERR:
    Serial.println("RANGE ERR: System did not converge before the specified max!");
    break;
  case VL6180X_IGNORE_ERR:
    Serial.println("RANGE ERR: Ignore threshold check failed !");
    break;
  case VL6180X_MAX_S_N_ERR:
    Serial.println("RANGE ERR: Measurement invalidated!");
    break;
  case VL6180X_RAW_Range_UNDERFLOW_ERR:
    Serial.println("RANGE ERR: RESULT_RANGE_RAW < 0!");
    break;
  case VL6180X_RAW_Range_OVERFLOW_ERR:
    Serial.println("RESULT_RANGE_RAW is out of range !");
    break;
  case VL6180X_Range_UNDERFLOW_ERR:
    Serial.println("RANGE ERR: RESULT__RANGE_VAL < 0 !");
    break;
  case VL6180X_Range_OVERFLOW_ERR:
    Serial.println("RANGE ERR: RESULT__RANGE_VAL is out of range !");
    break;
  default:
    Serial.println("RANGE ERR: Systerm err!");
    break;
  }
delay(1000);
}
