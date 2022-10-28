/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             leds.c
* Description:      Functions for controlling LEDs on μC board
*					Implementation file
* 
*/


// ==== INCLUDES ====
#include "leds.h"
// ==== INCLUDES ====


// ==== FUNCTION IMPLEMENTATIONS ====
void LEDsInit(void) {
	GPIOInit(LED_1, GPIO_DIR_OUTPUT);
	GPIOInit(LED_2, GPIO_DIR_OUTPUT);
	GPIOInit(LED_3, GPIO_DIR_OUTPUT);
	GPIOInit(LED_4, GPIO_DIR_OUTPUT);	
}

void LEDsOff(void) {
	PinWrite(LED_1, 1);
	PinWrite(LED_2, 1);
	PinWrite(LED_3, 0);
	PinWrite(LED_4, 0);
}
// ==== FUNCTION IMPLEMENTATIONS ====
