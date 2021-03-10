/**!
 * @file pollMeasurement.ino
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
DFRobot_VL6180X VL6180X;
#if defined(ESP32) || defined(ESP8266)
#define CE  D5
#elif defined(__AVR__) || defined(ARDUINO_SAM_ZERO)
#define CE  8
#elif (defined NRF5)
#define CE 9
#endif
void setup() {
  Serial.begin(9600);
  while(!(VL6180X.begin(/*pin*/CE))){
    Serial.println("Please check that the IIC device is properly connected!");
    delay(1000);
  }  
  VL6180X.setIICAddr(0x39);
  /** 
   * 20   times gain: VL6180X_ALS_GAIN_20                       
   * 10   times gain: VL6180X_ALS_GAIN_10                       
   * 5    times gain: VL6180X_ALS_GAIN_5                        
   * 2.5  times gain: VL6180X_ALS_GAIN_2_5                      
   * 1.57 times gain: VL6180X_ALS_GAIN_1_67                     
   * 1.27 times gain: VL6180X_ALS_GAIN_1_25                     
   * 1    times gain: VL6180X_ALS_GAIN_1                        
   * 40   times gain: VL6180X_ALS_GAIN_40                       
   */
  VL6180X.setALSGain(VL6180X_ALS_GAIN_1);
}

void loop() {
  // put your main code here, to run repeatedly:
  float lux = VL6180X.alsPoLLMeasurement();
  String str ="ALS: "+String(lux)+" lux";
  Serial.println(str);
  delay(1000);
  uint8_t range = VL6180X.rangePollMeasurement();
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
