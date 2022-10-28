/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             gpio.c
* Description:      General purpose input/output wrappers and unwrappers.
*                   Implementation file
* 
*/


// ==== INCLUDES ====
#include "gpio.h"
// ==== INCLUDES ====


// ==== FUNCTION IMPLEMENTATIONS ====

// Private functions (unwrapper)
static uint32_t GetPort(uint32_t port_pin) {
    return(port_pin >> 16);
}

static uint32_t GetPin(uint32_t port_pin) {
    return(port_pin & 0xFFFF);
}

// Public functions (wrappers)
void GPIOInit(uint32_t port_pin , uint32_t dir) {
    GPIOSetDir(GetPort(port_pin),GetPin(port_pin),dir);
}

void GPIOPinConfig(uint32_t port_pin , uint32_t config) {
    PINConfigure(GetPort(port_pin),GetPin(port_pin),config);
}

uint32_t PinRead(uint32_t port_pin) {
    return GPIOPinRead(GetPort(port_pin),GetPin(port_pin));
}

void PinWrite(uint32_t port_pin , uint32_t set) {
    GPIOPinWrite(GetPort(port_pin),GetPin(port_pin),set);
}
// ==== FUNCTION IMPLEMENTATIONS ====