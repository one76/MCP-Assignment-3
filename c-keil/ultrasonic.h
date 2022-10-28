/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             ultrasonic.h
* Description:      Functions to read in from the ultrasonic sensor and to
*					determine whether an object was detected or not.
* 
*/

#ifndef ULTRASONIC_H
#define ULTRASONIC_H


// ==== INCLUDES ====
#include <stdint.h>
// ==== INCLUDES ====


typedef struct {
	uint8_t detected;
	uint16_t range;
	int16_t angle;
} US_Typedef;


// ==== FUNCTION HEADERS ====
/** Ultrasonic Init
*	@brief Initialises ultrasonic sensor input
*/
void UltrasonicInit(void);

/** Ultrasonic Read
*	@brief Reads in data from ultrasoni sensor
*	@return [uint16_t] distance to detected object in mm
*/
uint16_t UltrasonicRead(void);

/** Ultrasonic Detect
*	@brief Determines whether an object is detected or not
*	@param object the detected object
*/
void UltrasonicDetect(US_Typedef* object);
// ==== FUNCTION HEADERS ====


#endif
