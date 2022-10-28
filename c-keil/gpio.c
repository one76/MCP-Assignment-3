#include "gpio.h"
// Private functions (unwrapper)
static uint32_t Get_Port(uint32_t port_pin) {
return(port_pin >> 16);
}
static uint32_t Get_Pin(uint32_t port_pin) {
return(port_pin & 0xFFFF);
}
// Public functions (wrappers)
void GPIO_Init(uint32_t port_pin , uint32_t dir) {
GPIO_SetDir(Get_Port(port_pin),Get_Pin(port_pin),dir);
}
void GPIO_Pin_Config(uint32_t port_pin , uint32_t config) {
PIN_Configure(Get_Port(port_pin),Get_Pin(port_pin),config);
}
uint32_t Pin_Read(uint32_t port_pin) {
return GPIO_PinRead(Get_Port(port_pin),Get_Pin(port_pin));
}
void Pin_Write(uint32_t port_pin , uint32_t set) {
GPIO_PinWrite(Get_Port(port_pin),Get_Pin(port_pin),set);
}
