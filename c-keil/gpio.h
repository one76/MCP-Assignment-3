/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:				gpio.h
* Description:		General purpose input/output wrappers and unwrappers
* 
*/

#ifndef GPIO_H
#define GPIO_H


// ==== INCLUDES ====
// GPIO and Pin header files
#include "GPIO_LPC40xx.h"
#include "PIN_LPC40xx.h"

// We adpot the standard integer defintions of the GPIO
// and Pin header files to avoid type warnings/errors
#include <stdint.h>
// ==== INCLUDES ====


// ==== FUNCTION HEADERS ====
/* Wrapper functions for useful functions within GPIO_LPC40xx.h
and PIN_LPC40xx.h. These functions take the peripheral
port_pin definition (e.g. LED_1) as a single macro.
*/

/** GPIO Init: 
	@brief Configure GPIO pin direction
	@param[in] port_num GPIO number (0..5)
	@param[in] pin_num Port pin number (0..31)
	@param[in] dir GPIO_DIR_INPUT , GPIO_DIR_OUTPUT
*/
void GPIOInit(uint32_t port_pin , uint32_t dir);

/** GPIO Pin Config: 
	@brief Set pin function and electrical characteristics
	@param[in] port port number (0..5)
	@param[in] pin pin number (0..31)
	@param[in] pin_cfg pin_cfg configuration bit mask
	@returns
	- @b 0: function succeeded
	- @b -1: function failed
*/
void GPIOPinConfig(uint32_t port_pin , uint32_t config);

/** Pin Read: 
	@brief Read port pin
	@param[in] port_num GPIO number (0..5)
	@param[in] pin_num Port pin number (0..31)
	@return pin value (0 or 1)
*/
extern uint32_t PinRead(uint32_t port_pin);

/** Pin Write: 
	@brief Write port pin
	@param[in] port_num GPIO number (0..5)
	@param[in] pin_num Port pin number (0..31)
	@param[in] val Port pin value (0 or 1)
*/
void PinWrite(uint32_t port_pin , uint32_t set);
// ==== FUNCTION HEADERS ====


#endif
