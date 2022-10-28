/*
 *
 *  =========================
 * |     MCP Assignment 3     |
 * | Michael Laden - a1748876 |
 * | Michael Neill - a1764673 |
 *  =========================
 *
 * File:          main.c
 * Description:   Contains high-level kobuki algorithm
 */

#ifndef ADC_H
#define ADC_H

#include "gpio.h"
#include "pin_defs.h"
#include "PIN_LPC40xx.h"
#include "system_LPC407x_8x_177x_8x.h"

/*
Intialise the ADC.
*/
void ADCInit ( void );

/*
Read the ADC value from the channel selected.
@param channel Select the channel to read from the ADC.
@return [uint32_t] Data from the ADC channel.
*/
uint32_t ADC_Read ( uint8_t channel );

#endif
