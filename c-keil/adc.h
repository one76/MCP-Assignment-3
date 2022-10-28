#ifndef ADC_H
#define ADC_H

#include "gpio.h"
#include "pin_defs.h"
#include "PIN_LPC40xx.h"
#include "system_LPC407x_8x_177x_8x.h"

void ADC_Init ( void );
uint32_t ADC_Read ( uint8_t channel );

#endif
