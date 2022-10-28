#include "joystick.h"

void Joystick_Init(void) {
	GPIO_Pin_Config(JOY_LT, IOCON_MODE_PULLUP);
	GPIO_Pin_Config(JOY_RT, IOCON_MODE_PULLUP);
	GPIO_Pin_Config(JOY_UP, IOCON_MODE_PULLUP);
	GPIO_Pin_Config(JOY_DN, IOCON_MODE_PULLUP);
	GPIO_Pin_Config(JOY_CR, IOCON_MODE_PULLUP);
	
	GPIO_Init(JOY_LT, GPIO_DIR_INPUT);
	GPIO_Init(JOY_RT, GPIO_DIR_INPUT);
	GPIO_Init(JOY_UP, GPIO_DIR_INPUT);
	GPIO_Init(JOY_DN, GPIO_DIR_INPUT);
	GPIO_Init(JOY_CR, GPIO_DIR_INPUT);
}
