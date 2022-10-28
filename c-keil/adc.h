/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             adc.h
* Description:      Enable the microcontroller to initialise and read from the ADC from the selected channel. 
* 
*/


#ifndef ADC_H
#define ADC_H

// ==== INCLUDES ====
#include "gpio.h"
#include "pin_defs.h"
#include "PIN_LPC40xx.h"
#include "system_LPC407x_8x_177x_8x.h"
// ==== INCLUDES ====


// ==== FUNCTION HEADERS ====
/** ADC Init
    @brief Intialise the ADC.
*/
void ADCInit ( void );

/** ADC READ
    @brief Read the ADC value from the channel selected.
    @param channel Select the channel to read from the ADC.
    @return [uint32_t] Data from the ADC channel.
*/
uint32_t ADCRead ( uint8_t channel );
// ==== FUNCTION HEADERS ====


#endif
