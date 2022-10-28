#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <stdint.h>

typedef struct {
    uint8_t detected;
		uint16_t range;
		int16_t angle;
} US_Typedef;

void Ultrasonic_Init(void);
uint16_t Ultrasonic_Read(void);
void Ultrasonic_Detect(US_Typedef* object);

#endif
