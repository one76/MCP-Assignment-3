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


// ==== INCLUDES ====
#include "adc.h"
#include "uart.h"
#include "kobuki.h"
#include "ultrasonic.h"
// ==== INCLUDES ====


// ==== MACROS ====
#define TRUE 1
#define FALSE 0
// ==== MACROS ====


// ==== STATES ====
enum {IDLE, SEARCH, FOUND, OBJECT, OBSTACLE, ROTATE} state;
// ==== STATES ====


int main() {
    // Objects
    Kobuki_Typedef kobuki   = {};
    US_Typedef object       = {};

    // For Storing States
    int collected_rocks[2] = {0,0};
    int DIR = CCW;
		int prev_range=0;

    // Boolean flag
		int COLLECTING_FIRST_ROCK = collected_rocks[0] == FALSE;
        int KEEP_SEARCHING = !(!COLLECTING_FIRST_ROCK || (COLLECTING_FIRST_ROCK && object.range<850)) ? FALSE : TRUE;
		int LAYOUT_3 = FALSE;
		int STOP_KOBUKI = FALSE;
		int FOUND_NEW_ROCK = 0;
		
    // Init
    ADC_Init();
    UART_Init();
    Ultrasonic_Init();


    while(1) {
        
        // Update Sensor Values
        Kobuki_Read(&kobuki);
        Ultrasonic_Detect(&object);
        
        // Boolean Flags to Increase Readablility
        STOP_KOBUKI = (
                kobuki.button == BUTTON_1   
                //kobuki.wheeldrop            
            );
        COLLECTING_FIRST_ROCK = collected_rocks[0] == FALSE;
				FOUND_NEW_ROCK= !(object.range>=prev_range-200 && object.range<=prev_range+200);
					
				
        switch (state)
        {
        case IDLE:
            if (kobuki.button == BUTTON_0)
            {
                state = SEARCH;
            }
            else {
                Kobuki_Drive(STOP);
								Kobuki_Rotate(STOP);
            }
            break;
						
        case SEARCH:
            if (kobuki.button == BUTTON_1) {
                state=IDLE;
            }
            else if (object.detected && FOUND_NEW_ROCK) {
								prev_range=object.range;
								Kobuki_Rotate(STOP);
                state = FOUND;
            }
            else if (kobuki.bumper || kobuki.cliff) {
								Kobuki_Rotate(STOP);
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
								Kobuki_Rotate_Angle_To_Completion((int16_t)11*DIR, kobuki);
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
								if (object.range <= 60) state=IDLE;
								// state=IDLE;
							}
						}
						if (kobuki.bumper) {
							collected_rocks[0] = TRUE;
							state=IDLE;
						}
						if (kobuki.cliff) {
							if (!COLLECTING_FIRST_ROCK) {
								LAYOUT_3=TRUE;
							}
							state=OBSTACLE;
						}
						if (!object.detected && !kobuki.bumper && !kobuki.cliff) {
							state=SEARCH;
						}
            break;
						
        case OBSTACLE:
					if (STOP_KOBUKI) {
                state=IDLE;
            }
					if (!kobuki.bumper && !kobuki.cliff) {
						state=SEARCH;
					}
					else {
						Kobuki_Drive_To_Completion((int16_t)-80, kobuki);
						if (kobuki.cliff && !LAYOUT_3) {
							Kobuki_Rotate_Angle_To_Completion((int16_t)60*CW, kobuki);
							Kobuki_Drive_To_Completion((int16_t)250, kobuki);
						}
						else if (kobuki.cliff && LAYOUT_3) {
							Kobuki_Rotate_Angle_To_Completion((int16_t)100*CW, kobuki);
							Kobuki_Drive_To_Completion((int16_t)700, kobuki);
							Kobuki_Rotate_Angle_To_Completion((int16_t)100*CW, kobuki);
							Kobuki_Drive_To_Completion((int16_t)500, kobuki);
						}
						
					}
						
            break;
        }
    }
        
}