/**!
 * @file restart.ino
 * @brief 该示例会重置传感器，并把I2C地址恢复为默认（0x29）
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence     The MIT License (MIT)
 * @author [yangfeng]<feng.yang@dfrobot.com>
 * @version  V1.0
 * @date  2021-02-08
 * @get from https://www.dfrobot.com
 * @url  https://github.com/DFRobot/DFRobot_VL6180X
 */
 uint8_t Pin 12   //设置的GPIO口与传感器的CE引脚相连
void setup() {
 pinMode(pin,OUTPUT);
 digitalWrite(Pin,LOW);
 delayMicroseconds(300);
 digitalWrite(Pin,HIGH);
}

void loop() {

}
