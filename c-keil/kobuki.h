/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             kobuki.h
* Description:      Kobuki functions for transferring and receiving information 
*                   from and to the kobuki. Also, functions for controlling the
*                   kobuki.
*
*/


#ifndef KOBUKI_H
#define KOBUKI_H


// ==== INCLUDES ====
#include <stdint.h>
// ==== INCLUDES ====


// ==== MACROS ====
#define SPEED_LIMIT (int16_t)150 //mm/s
#define SEARCH_SPEED (int16_t)75 // mm/s
#define STOP    0
#define CCW     1   // Counter-clockwise
#define CW      -1  // Clockwise
#define BUTTON_0 0x01
#define BUTTON_1 0x02
#define BUTTON_2 0x04
// ==== MACROS ====


typedef enum {OFF , RED , GREEN , YELLOW} Kobuki_LED_Enum;

typedef struct {
    uint8_t     cliff;
    uint8_t     bumper;
    uint8_t     wheeldrop;
    uint8_t     button;
	uint16_t    distance;
    int16_t     angle;
    uint8_t     rotation_complete;
    uint8_t     distance_complete;
} Kobuki_Typedef;

static volatile int32_t		setpoint_distance_tick;
static volatile int16_t		setpoint_angle_deg;
static uint8_t		        rotation_complete = 1;
static uint8_t		        distance_complete = 1;


// ==== FUNCTION HEADERS ====
/** KobukiRx
*   @brief
*   @param
*   @return
*/
uint8_t KobukiRx(uint8_t* , uint32_t);

/**
*   @brief
*   @param
*   @return
*/
void KobukiTx(uint8_t*, uint8_t);

/**
*   @brief
*   @param
*   @return
*/
void KobukiRead(Kobuki_Typedef*);

/**
*   @brief
*   @param
*   @return
*/
void KobukiRotateOrDrive(int16_t speed, int mode);

/**
*   @brief
*   @param
*   @return
*/
void KobukiRotate(int16_t speed);

/**
*   @brief
*   @param
*   @return
*/
void KobukiDrive(int16_t speed);

/**
*   @brief
*   @param
*   @return
*/
void KobukiDriveDistance(uint16_t current_distance_tick);

/**
*   @brief
*   @param
*   @return
*/
void KobukiDriveDistanceSetpoint(uint16_t current_distance_tick, int16_t distance);

/**
*   @brief
*   @param
*   @return
*/
void KobukiDriveToCompletion(int16_t distance, Kobuki_Typedef kobuki);

/**
*   @brief
*   @param
*   @return
*/
void KobukiRotateAngleSetpoint(int16_t current_angle_tick, int16_t rot_angle_deg);

/**
*   @brief
*   @param
*   @return
*/
void KobukiRotateAngle(int16_t current_angle_tick);

/** Kobuki Rotate Angle to Completion: 
*   @brief Rotates the kobuki a specified angle in deg. Functions
*   complete only once rotation_complete is false (0). Therefore
*   cannot check sensors while rotating so be careful when using!
*   @param rot_angle_deg angle to rotate by in degrees. Note: positive
*   angle is CCW and negative angle is CW.
*   @return
*/
void KobukiRotateAngleToCompletion(int16_t rot_angle_deg, Kobuki_Typedef kobuki);

/** Kobuki Update LEDs: 
*   @brief Updates the 2 programmable LEDs on the kobuki
*   @param led_1_colour 1st LED colour
*   @param led_2_colour 2nd LED colour
*/
void KobukiUpdateLEDs(int8_t led_1_colour, int8_t led_2_colour);
// ==== FUNCTION HEADERS ====


#endif
