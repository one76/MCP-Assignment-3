/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             leds.h
* Description:      Functions for controlling LEDs on μC board
* 
*/

#ifndef LEDS_H
#define LEDS_H

// ==== INCLUDES ====
// Include pin defintions and wrapper functions
#include "gpio.h"
#include "pin_defs.h"
// ==== INCLUDES ====


// ==== FUNCTION HEADERS ====
// Uses the functions GPIOInit and PinWrite
// Requires LED_1 , LED_2 , LED_3 , LED_4

/** LEDs Init
	@brief Initialise the 4 LEDs.
	-Set all the pin directions
*/
void LEDsInit(void);

/** LEDs Off
	@brief Turn off the 4 LEDs.
	-Write to all 4 LEDs
*/
void LEDsOff(void);
// ==== FUNCTION HEADERS ====


#endif
