/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:          	ultrasonic.c
* Description:		Functions to read in from the ultrasonic sensor and to
*					determine whether an object was detected or not.
*                   Implementation file.
* 
*/

// ==== INCLUDES ====
#include "ultrasonic.h"
#include "pin_defs.h"
#include "gpio.h"
#include "adc.h"
// ==== INCLUDES ====


// ==== MACROS ====
#define DETECT_RANGE 2500 //mm
#define SUPPLY_VOLTAGE 3.3
#define MM_PER_V (1024*5.0/SUPPLY_VOLTAGE)
#define INT_TO_MM(adc_val) (adc_val/( (float)0xFFF ))*3.3f*MM_PER_V
#define OFFSET 410
// ==== MACROS ====


// ==== FUNCTION IMPLEMENTATIONS ====
void UltrasonicInit(void) {
    GPIOPinConfig ( ULTRASONIC_ADC_1 , 0x001 | // FUNCT - IOCON control register
                    IOCON_ANALOG_MODE ); // ADMODE - IOCON register bit description <- what is this?
}

uint16_t UltrasonicRead(void) {
    uint32_t adc_val = ADCRead(ULTRASONIC_CHANNEL);
    uint16_t range = INT_TO_MM(adc_val);

    return range;
}

void UltrasonicDetect(US_Typedef* object) {
    uint16_t range = UltrasonicRead();
	object->range = range-OFFSET;

    if (range < DETECT_RANGE) {
        object->detected = 1; // TRUE
    }
    else {
        object->detected = 0; // FALSE
    }
}
// ==== FUNCTION IMPLEMENTATIONS ====
