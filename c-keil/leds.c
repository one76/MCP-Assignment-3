#include "leds.h"

void LEDs_Init(void) {
	GPIO_Init(LED_1, GPIO_DIR_OUTPUT);
	GPIO_Init(LED_2, GPIO_DIR_OUTPUT);
	GPIO_Init(LED_3, GPIO_DIR_OUTPUT);
	GPIO_Init(LED_4, GPIO_DIR_OUTPUT);	
}

void LEDs_Off(void) {
	Pin_Write(LED_1, 1);
	Pin_Write(LED_2, 1);
	Pin_Write(LED_3, 0);
	Pin_Write(LED_4, 0);
}
