// Motor control.
#include "motor.h"


// Initialise the motor pins in the 'output' direction as in Lab 2.
void Motor_Init(void){
	GPIO_Init(MOTOR_A1, GPIO_DIR_OUTPUT);
	GPIO_Init(MOTOR_A3, GPIO_DIR_OUTPUT);
	GPIO_Init(MOTOR_B1, GPIO_DIR_OUTPUT);
	GPIO_Init(MOTOR_B3, GPIO_DIR_OUTPUT);
}

// Function to turn the motor off
void Motor_Off(void){
	// Set all motor pins to zero
	Pin_Write(MOTOR_A1, 0);
	Pin_Write(MOTOR_A3, 0);
	Pin_Write(MOTOR_B1, 0);
	Pin_Write(MOTOR_B3, 0);
}

// Function to drive the motor. This uses the sequence defined by the wiring diagram file
void Motor_Drive(int* step, int dir_state){
	
	if(*step == 0){
		Pin_Write(MOTOR_A1, 1);
		Pin_Write(MOTOR_B3, 1);
	}
	else if(*step == 1){
		Pin_Write(MOTOR_A1, 1);
		Pin_Write(MOTOR_B1, 1);
	}
	else if(*step == 2){
		Pin_Write(MOTOR_A3, 1);
		Pin_Write(MOTOR_B1, 1);
	}
	else if(*step == 3){
		Pin_Write(MOTOR_A3, 1);
		Pin_Write(MOTOR_B3, 1);
	}
	
	if(dir_state == CLOCKWISE){
		*step = (*step+1) % NO_STEPS;
	}
	else{
		*step = (*step-1+NO_STEPS) % NO_STEPS;
	}
}
