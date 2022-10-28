#ifndef MOTOR_H
#define MOTOR_H
// Include pin defintions and wrapper functions

#include "gpio.h"
#include "pin_defs.h"

// Macros definitions for motor states
#define COUNTERCLOCKWISE 0
#define CLOCKWISE 1

// Number of steps per pole
#define NO_STEPS 4

// Uses the functions GPIO_Pin_Config and GPIO_Init
// Requires MOTOR_A1 , MOTOR_A3 , MOTOR_B1 , MOTOR_B3
/**
	\fn void Motor_Init(void)
	\brief Initialise the 4 motor drive channels.
	-Set all the pin directions
*/
void Motor_Init(void);

/**
	\fn void Motor_Off(void)
	\brief Turn off the control signals to the motor.
	-Write to both pins of the A & B phases
*/
void Motor_Off(void);

/**
	\fn void Motor_Off(void)
	\brief Turn off the control signals to the motor.
	-Write to both pins of the A & B phases
	\param current motor step 0..3
	\param motor direction COUNTERCLOCKWISE or CLOCKWISE
	\return new step (+1 CW, -1 CCW)
*/
extern void Motor_Drive(int* step ,int dir_state);

#endif
