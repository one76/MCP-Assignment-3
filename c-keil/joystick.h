#ifndef JOYSTICK_H
#define JOYSTICK_H

// Include pin defintions and wrapper functions
#include "gpio.h"
#include "pin_defs.h"

// Uses the functions GPIO_Pin_Config and GPIO_Init
// Requires JOY_LT , JOY_RT , JOY_UP , JOY_DN , JOY_CR

/**
	\fn void Joystick_Init(void)
	\brief Initialise the 5 Joystick pins.
	(1) Configure all the pins
	(2) Set all the pin directions
*/
void Joystick_Init(void);

#endif
