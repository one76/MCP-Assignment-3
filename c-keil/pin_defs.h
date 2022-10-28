/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             pin_defs.h
* Description:      Contains pin definition macros for μC inputs and outputs
* 
*/

#ifndef PIN_DEFS_H
#define PIN_DEFS_H

// Define peripherals to be used on LPC4088 QSB & Exper BB
// We use the structure: (port << 16) | pin

// QSB LEDs
#define LED_1 (1 << 16) | 18 // Px_xx
#define LED_2 (0 << 16) | 13 // Px_xx
#define LED_3 (1 << 16) | 13 // Px_xx
#define LED_4 (2 << 16) | 19 // Px_xx

// Define ultrasonic ADC pin and channel
#define ULTRASONIC_ADC_1 (0 << 16) | 24 // Page 139 and LPC4088 Experiment BB Circuit Diagrams ADC0_IN[1]
#define ULTRASONIC_CHANNEL 1

#endif
