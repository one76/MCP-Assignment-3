/* 
* 
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 | 
* | Michael Neill - a1764673 |
*  ========================= 
* 
* File: main.c
* Contains high-level kobuki algorithm
*/

// INCLUDES
#include "adc.h"
#include "uart.h"
#include "kobuki.h"
#include "ultrasonic.h"

// MACROS
#define TRUE 1
#define FALSE 0

// STATES
enum {IDLE, SEARCH, FOUND, OBJECT, OBSTACLE} state;

int main() {
    // Objects
    Kobuki_Typedef kobuki   = {};
    US_Typedef object       = {};

    // For Storing States
    int collected_rocks[2] = {0,0};
    int DIR = CCW;

    // Boolean flag
		int COLLECTING_FIRST_ROCK = collected_rocks[0] == FALSE;
    int KEEP_SEARCHING = !(!COLLECTING_FIRST_ROCK || (COLLECTING_FIRST_ROCK && object.range<850)) ? FALSE : TRUE;
		int LAYOUT_3 = FALSE;
		
    // Init
    ADC_Init();
    UART_Init();
    Ultrasonic_Init();


    while(1) {
        
        // Update Sensor Values
        Kobuki_Read(&kobuki);
        Ultrasonic_Detect(&object);
        
        // Boolean Flags to Increase Readablility
        int STOP_KOBUKI = (
                kobuki.button == BUTTON_1   ||
                kobuki.wheeldrop            
            );
        COLLECTING_FIRST_ROCK = collected_rocks[0] == FALSE;

				// ROTATE SET ANGLE TO COMPLETION
				while (kobuki.rotation_complete == 0) {
						Kobuki_Rotate_Angle(kobuki.angle);
				}
					
				
        switch (state)
        {
        case IDLE:
            if (kobuki.button == BUTTON_0)
            {
                state = SEARCH;
            }
            else {
                Kobuki_Drive(STOP);
            }
            break;
        case SEARCH:
            if (STOP_KOBUKI) {
                state=IDLE;
            }
            else if (object.detected) {
                state = FOUND;
            }
            else if (kobuki.bumper || kobuki.cliff) {
                state = OBSTACLE;
            }
            else if (!object.detected || (object.detected && KEEP_SEARCHING)) {
                Kobuki_Rotate(SEARCH_SPEED*DIR);
            }
            break;
        case FOUND:
            if (STOP_KOBUKI) {
                state = IDLE;
            }
						// Find closest rock
            else if (!COLLECTING_FIRST_ROCK || (COLLECTING_FIRST_ROCK && object.range<850)) {
                KEEP_SEARCHING=FALSE;
                Kobuki_Rotate_Angle_Setpoint(kobuki.angle, (int16_t)11*DIR);
								state = OBJECT;
            }
            else {
                KEEP_SEARCHING=TRUE;
                state=SEARCH;
            }
            break;
        case OBJECT:
						if (STOP_KOBUKI) {
                state = IDLE;
            }
						
						// Bumping 1st rock or stopping before 2nd rock
						if (object.detected && !kobuki.bumper && !kobuki.cliff) {
							// DRIVE TO OBJECT
							if (kobuki.distance_complete == 0) {
								Kobuki_Drive_Distance(kobuki.distance);
							}
							
							
							if (COLLECTING_FIRST_ROCK) {
								Kobuki_Drive_Distance_Setpoint(kobuki.distance, object.range);
							}
							else {
								Kobuki_Drive_Distance_Setpoint(kobuki.distance, object.range-60);
								state=IDLE;
							}
							
							if (kobuki.bumper) {
								collected_rocks[0] = TRUE;
								state=OBSTACLE;
							}
							if (kobuki.cliff) {
								if (!COLLECTING_FIRST_ROCK) {
									LAYOUT_3 =TRUE;
								}
								state=OBSTACLE;
							}
							if (!object.detected && !kobuki.bumper && !kobuki.cliff) {
								state=SEARCH;
							}
						}
            break;
        case OBSTACLE:
					if (STOP_KOBUKI) {
                state=IDLE;
            }
					if (
						(!(kobuki.bumper || kobuki.cliff) && 
						kobuki.distance_complete == TRUE &&
						kobuki.rotation_complete == TRUE)
						) {
						state=SEARCH;
					}
					else {
						Kobuki_Drive_Distance_Setpoint(kobuki.distance, (int16_t)-80);
						if (kobuki.cliff && !LAYOUT_3) {
							Kobuki_Rotate_Angle_Setpoint(kobuki.angle, (int16_t)60*CW);
							Kobuki_Drive_Distance_Setpoint(kobuki.distance, (int16_t)250);
						}
						else if (kobuki.cliff && LAYOUT_3) {
							Kobuki_Rotate_Angle_Setpoint(kobuki.angle, (int16_t)100*CW);
							Kobuki_Drive_Distance_Setpoint(kobuki.distance, (int16_t)700);
							Kobuki_Rotate_Angle_Setpoint(kobuki.angle, (int16_t)100*CW);
							Kobuki_Drive_Distance_Setpoint(kobuki.distance, (int16_t)500);
						}
						
					}
					if (kobuki.distance_complete == FALSE && kobuki.rotation_complete == TRUE) {
						Kobuki_Drive_Distance(kobuki.distance);
					}
						
            break;
        }
    }
        
}
