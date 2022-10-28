#ifndef GPIO_H
#define GPIO_H

// GPIO and Pin header files
#include "GPIO_LPC40xx.h"
#include "PIN_LPC40xx.h"

// We adpot the standard integer defintions of the GPIO
// and Pin header files to avoid type warnings/errors
#include <stdint.h>

/* Wrapper functions for useful functions within GPIO_LPC40xx.h
and PIN_LPC40xx.h. These functions take the peripheral
port_pin definition (e.g. LED_1) as a single macro.
*/

/**
	\fn void GPIO_Init (uint32_t port_num ,
	uint32_t pin_num ,
	uint32_t dir)
	\brief Configure GPIO pin direction
	\param[in] port_num GPIO number (0..5)
	\param[in] pin_num Port pin number (0..31)
	\param[in] dir GPIO_DIR_INPUT , GPIO_DIR_OUTPUT
*/
void GPIO_Init(uint32_t port_pin , uint32_t dir);

/**
	\fn int32_t GPIO_PIN_Config (uint32_t function) {
	\brief Set pin function and electrical characteristics
	\param[in] port port number (0..5)
	\param[in] pin pin number (0..31)
	\param[in] pin_cfg pin_cfg configuration bit mask
	\returns
	- \b 0: function succeeded
	- \b -1: function failed
*/
void GPIO_Pin_Config(uint32_t port_pin , uint32_t config);

/**
	\fn uint32_t Pin_Read (uint32_t port_num , uint32_t pin_num)
	\brief Read port pin
	\param[in] port_num GPIO number (0..5)
	\param[in] pin_num Port pin number (0..31)
	\return pin value (0 or 1)
*/
extern uint32_t Pin_Read(uint32_t port_pin);

/**
	\fn void Pin_Write (uint32_t port_num ,
	uint32_t pin_num ,
	uint32_t val);
	\brief Write port pin
	\param[in] port_num GPIO number (0..5)
	\param[in] pin_num Port pin number (0..31)
	\param[in] val Port pin value (0 or 1)
*/
void Pin_Write(uint32_t port_pin , uint32_t set);

#endif
