/**
 * @file alsContinuousInterruptMode.ino
 * @brief 本传感器工作可工作在四种中断模式下，分别是低于下阈值触发中断模式、高于上阈值触发中断模式、低于下阈值或者高于上阈值触发中断模式以及新样本值采集完成触发中断模式
 * @n 本示例介绍了在连续测量环境光模式下的四种中断
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
  flag = 1;
}
void setup() {
  Serial.begin(9600);
  while(!(VL6180X.begin(/*pin*/CE))){
    Serial.println("Please check that the IIC device is properly connected!");
    delay(1000);
  }
  /*配置环境光采集周期*/  
  VL6180X.alsSetInterMeasurementPeriod(/*uint16_t periodMs*/1000);

  /** 开启INT引脚的通知功能
   * mode：
   * VL6180X_DIS_INTERRUPT          不开启中断
   * VL6180X_LOW_INTERRUPT          开启中断，INT引脚默认输出低电平
   * VL6180X_HIGH_INTERRUPT         开启中断，INT引脚默认输出高电平
   * 注意：当使用VL6180X_LOW_INTERRUPT模式开启中断时，请用“RISING”来触发中断，当使用VL6180X_HIGH_INTERRUPT模式开启中断时，请用“FALLING”来触发中断。
   */
  VL6180X.setInterrupt(/*mode*/VL6180X_LOW_INTERRUPT); 

  /** 配置采集环境光的中断模式
   * mode 
   * interrupt disable  :                       VL6180X_INT_DISABLE             0
   * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
   * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
   * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
   * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
   */
  VL6180X.alsConfigInterrupt(/*mode*/VL6180X_NEW_SAMPLE_READY); 
  /**设置采集增益
   * gain:
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

  //这里设置阈值的接口和设置增益的接口相关联，若要同时指定增益和阈值，请先设置增益，再设置阈值
  VL6180X.setALSThresholdValue(/*thresholdL 0-65535 */40,/*thresholdH 0-65535*/50);
  
  #if defined(ESP32) || defined(ESP8266)||defined(ARDUINO_SAM_ZERO)
  attachInterrupt(digitalPinToInterrupt(D9)/*Query the interrupt number of the D9 pin*/,interrupt,RISING);
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
  attachInterrupt(/*Interrupt No*/0,interrupt,RISING);//Open the external interrupt 0, connect INT1/2 to the digital pin of the main control: 
    //UNO(2), Mega2560(2), Leonardo(3), microbit(P0).
  #endif
  
  /*开启连续采集模式*/
  VL6180X.alsStartContinuousMode();
}

void loop() {
  if(flag == 1){
    flag = 0;
    /*读取中断的状态*/
    uint8_t state = VL6180X.alsGetInterruptStatus();  
    /**  state  与设置的中断模式相对应
     * interrupt disable  :                       VL6180X_INT_DISABLE             0
     * value < thresh_low :                       VL6180X_LEVEL_LOW               1 
     * value > thresh_high:                       VL6180X_LEVEL_HIGH              2
     * value < thresh_low OR value > thresh_high: VL6180X_OUT_OF_WINDOW           3
     * new sample ready   :                       VL6180X_NEW_SAMPLE_READY        4
     */
    if(state == VL6180X_NEW_SAMPLE_READY){
      /*获得采集数据*/
      float lux = VL6180X.alsGetMeasurement();
      /*清除中断*/
      VL6180X.clearAlsInterrupt();
      String str ="ALS: "+String(lux)+" lux";
      Serial.println(str);
    }
  }
}
