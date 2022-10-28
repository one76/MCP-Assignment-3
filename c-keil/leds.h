#ifndef LEDS_H
#define LEDS_H

// Include pin defintions and wrapper functions
#include "gpio.h"


#include "pin_defs.h"
// Uses the functions GPIO_Init and Pin_Write
// Requires LED_1 , LED_2 , LED_3 , LED_4

/**
	\fn LEDs_Init(void)
	\brief Initialise the 4 LEDs.
	-Set all the pin directions
*/
void LEDs_Init(void);

/**
	\fn void LEDs_Off(void)
	\brief Turn off the 4 LEDs.
	-Write to all 4 LEDs
*/
void LEDs_Off(void);

#endif
