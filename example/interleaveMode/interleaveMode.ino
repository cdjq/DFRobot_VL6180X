/**
 * @file interleaveMode.ino
 * @brief 本示例介绍了在交叉测量模式下的进行中断方式的测量光照数据以及范围数据。
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2021-03-08
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_VL6180X
 */
#include <DFRobot_VL6180X.h>
DFRobot_VL6180X VL6180X;
uint8_t flag = 0;
uint8_t ret= 1;
#if defined(ESP32) || defined(ESP8266)
#define CE  D5
#elif defined(__AVR__) || defined(ARDUINO_SAM_ZERO)
#define CE  8
#elif (defined NRF5)
#define CE 9
#endif
void interrupt()
{
  if(flag ==0){
    flag = 1;
  }
}
void setup() {
  Serial.begin(9600);
  while(!(VL6180X.begin(/*pin*/CE))){
    Serial.println("Please check that the IIC device is properly connected!");
    delay(1000);
  }  
  /** mode
   * VL6180X_DIS_INTERRUPT          不开启中断
   * VL6180X_LOW_INTERRUPT          开启中断，INT引脚默认输出低电平
   * VL6180X_HIGH_INTERRUPT         开启中断，INT引脚默认输出高电平
   * 注意：当使用VL6180X_LOW_INTERRUPT模式开启中断时，请用“RISING”来触发中断，当使用VL6180X_HIGH_INTERRUPT模式开启中断时，请用“FALLING”来触发中断。
   */
  VL6180X.setInterrupt(/*mode*/VL6180X_HIGH_INTERRUPT); 

  /** mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
   */
  VL6180X.alsConfigInterrupt(/*mode*/VL6180X_NEW_SAMPLE_READY); 
 /** mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
   */
  VL6180X.rangeConfigInterrupt(VL6180X_NEW_SAMPLE_READY);
  VL6180X.alsSetInterMeasurementPeriod(1000);

  #if defined(ESP32) || defined(ESP8266)||defined(ARDUINO_SAM_ZERO)
  attachInterrupt(digitalPinToInterrupt(D9)/*Query the interrupt number of the D9 pin*/,interrupt,FALLING);
  #else
  /*    The Correspondence Table of AVR Series Arduino Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------
   * |                                        |  DigitalPin  | 2  | 3  |                   |
   * |    Uno, Nano, Mini, other 328-based    |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  |                   |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 2  | 3  | 21 | 20 | 19 | 18 |
   * |               Mega2560                 |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  | 5  |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 3  | 2  | 0  | 1  | 7  |    |
   * |    Leonardo, other 32u4-based          |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  |    |
   * |--------------------------------------------------------------------------------------
   */
  /*                      The Correspondence Table of micro:bit Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------------------------------------------------------------
   * |             micro:bit                       | DigitalPin |P0-P20 can be used as an external interrupt                                     |
   * |  (When using as an external interrupt,      |---------------------------------------------------------------------------------------------|
   * |no need to set it to input mode with pinMode)|Interrupt No|Interrupt number is a pin digital value, such as P0 interrupt number 0, P1 is 1 |
   * |-------------------------------------------------------------------------------------------------------------------------------------------|
   */
  attachInterrupt(/*Interrupt No*/0,interrupt,FALLING);//Open the external interrupt 0, connect INT1/2 to the digital pin of the main control: 
    //UNO(2), Mega2560(2), Leonardo(3), microbit(P0).
  #endif
  /**
   * 这里用来确保连续模式的关闭，但是这里会触发一次单次测量模式下的测量
   */

  
  VL6180X.startInterleavedMode();

}

void loop() {
  if(flag == 1){
    /** state 与设置的中断模式相对应
     * No threshold events reported  :                                            0
     * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
     * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
     * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
     * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
     */
    if(VL6180X.alsGetInterruptStatus() == VL6180X_NEW_SAMPLE_READY){
      float lux = VL6180X.alsGetMeasurement();
      VL6180X.clearAlsInterrupt();
      String str ="ALS: "+String(lux)+" lux";
      Serial.println(str);
      flag = 0;
    }
    if(VL6180X.rangeGetInterruptStatus() == VL6180X_NEW_SAMPLE_READY){
      flag = 0;
      uint8_t range = VL6180X.rangeGetMeasurement();
      uint8_t status = VL6180X.getRangeResult();
      VL6180X.clearRangeInterrupt();
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
    }
  }
}
