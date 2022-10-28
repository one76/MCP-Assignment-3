#ifndef UART3_H
#define UART3_H

#include "gpio.h"
#include "PIN_LPC40xx.h"
#include "system_LPC407x_8x_177x_8x.h"

void UART_Init(void);
uint8_t UART_Rx(void);
void UART_Tx(uint8_t byte);

#endif
