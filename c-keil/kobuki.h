#ifndef KOBUKI_H
#define KOBUKI_H

#include <stdint.h>

#define SPEED_LIMIT (int16_t)150 //mm/s
#define SEARCH_SPEED (int16_t)75 // mm/s
#define STOP 0
#define CCW 1
#define CW -1
#define BUTTON_0 0x01
#define BUTTON_1 0x02
#define BUTTON_2 0x04

typedef enum {OFF , RED , GREEN , YELLOW} Kobuki_LED_Enum;

typedef struct {
    uint8_t cliff;
    uint8_t bumper;
    uint8_t wheeldrop;
    uint8_t button;
	  uint16_t distance;
    int16_t angle;
    uint8_t rotation_complete;
    uint8_t distance_complete;
} Kobuki_Typedef;

static volatile int32_t		setpoint_distance_tick;
static volatile int16_t		setpoint_angle_deg;
static					uint8_t		rotation_complete = 1;
static					uint8_t		distance_complete = 1;

// ROUTINES

uint8_t Kobuki_Rx(uint8_t* , uint32_t);
void Kobuki_Tx(uint8_t*, uint8_t);
void Kobuki_Read(Kobuki_Typedef*);
void Kobuki_Rotate_Or_Drive(int16_t speed, int mode);
void Kobuki_Rotate(int16_t speed);
void Kobuki_Drive(int16_t speed);
void Kobuki_Drive_Distance(uint16_t current_distance_tick);
void Kobuki_Drive_Distance_Setpoint(uint16_t current_distance_tick, int16_t distance);
void Kobuki_Drive_To_Completion(int16_t distance, Kobuki_Typedef kobuki);
void Kobuki_Rotate_Angle_Setpoint(int16_t current_angle_tick, int16_t rot_angle_deg);
void Kobuki_Rotate_Angle(int16_t current_angle_tick);
void Kobuki_Rotate_Angle_To_Completion(int16_t rot_angle_deg, Kobuki_Typedef kobuki);

void Kobuki_Update_LEDs(int8_t led_1_colour, int8_t led_2_colour);

#endif
