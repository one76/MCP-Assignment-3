/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             uart.h
* Description:      UART serial communication functions
* 
*/


#ifndef UART3_H
#define UART3_H


// ==== INCLUDES ====
#include "gpio.h"
#include "PIN_LPC40xx.h"
#include "system_LPC407x_8x_177x_8x.h"
// ==== INCLUDES ====


// ==== FUNCTION HEADERS ====
/** UART Init: 
*   @brief Initialises UART
*/
void UARTInit(void);

/** UART Rx: 
*   @brief Recieves information via UART serial communication
*   @return [uint8_t] information read in
*/
uint8_t UARTRx(void);

/** UART Tx: 
*   @brief Sends information via UART serial communication
*   @param byte information to be sent
*/
void UARTTx(uint8_t byte);
// ==== FUNCTION HEADERS ====


#endif
