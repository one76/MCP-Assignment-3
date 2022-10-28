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
*
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
    int collected_rocks[2]  = {0,0};
    int DIR                 = CCW;
	int prev_range          = 0;

    // Boolean flag
    int collecting_first_rock   = collected_rocks[0] == FALSE;
    int keep_searching          = (!collecting_first_rock || (collecting_first_rock && object.range<850)) ? TRUE : FALSE;
    int LAYOUT_3                = FALSE;
    int stop_kobuki             = FALSE;
    int found_new_rock          = 0;
		
    // Init
    ADCInit();
    UARTInit();
    UltrasonicInit();


    while(1) {
        
        // Update Sensor Values
        KobukiRead(&kobuki);
        UltrasonicDetect(&object);
        
        // Boolean Flags to Increase Readablility
        stop_kobuki = (
            kobuki.button == BUTTON_1   
            kobuki.wheeldrop            
        );
        collecting_first_rock   = collected_rocks[0] == FALSE;
		found_new_rock          = !(object.range>=prev_range-200 && object.range<=prev_range+200);
					
        switch (state)
        {
        case IDLE:
            if (kobuki.button == BUTTON_0) {
                state = SEARCH;
            }
            else {
                KobukiDrive(STOP);
				KobukiRotate(STOP);
            }
            break;
    
        case SEARCH:
            if (kobuki.button == BUTTON_1) {
                state = IDLE;
            }
            else if (object.detected && found_new_rock) {
				prev_range = object.range;
				KobukiRotate(STOP);
                state = FOUND;
            }
            else if (kobuki.bumper || kobuki.cliff) {
				KobukiRotate(STOP);
                state = OBSTACLE;
            }
            else if (!object.detected || (object.detected && keep_searching)) {
                KobukiRotate(SEARCH_SPEED*DIR);
            }
            break;
						
        case FOUND:
            if (stop_kobuki) {
                state = IDLE;
            }
			// Find closest rock
            else if (!collecting_first_rock || (collecting_first_rock && object.range<850)) {
                keep_searching = FALSE;
                KobukiRotateAngleToCompletion((int16_t)11*DIR, kobuki);
                state = OBJECT;
            }
            else {
                keep_searching = TRUE;
                state = SEARCH;
            }
            break;
						
        case OBJECT:
			if (stop_kobuki) {
                state = IDLE;
            }
						
            // Bumping 1st rock or stopping before 2nd rock
            if (object.detected && !kobuki.bumper && !kobuki.cliff) {
                // DRIVE TO OBJECT
                if (kobuki.distance_complete == 0) {
                    KobukiDriveDistance(kobuki.distance);
                }
                
                
                if (collecting_first_rock) {
                    KobukiDriveDistanceSetpoint(kobuki.distance, object.range);
                }
                else {
                    KobukiDriveDistanceSetpoint(kobuki.distance, object.range-60);
                    if (object.range <= 60) state=IDLE;
                }
            }

            if (kobuki.bumper) {
                collected_rocks[0] = TRUE;
                state = IDLE;
            }
            if (kobuki.cliff) {
                if (!collecting_first_rock) {
                    LAYOUT_3 = TRUE;
                }
                state = OBSTACLE;
            }
            if (!object.detected && !kobuki.bumper && !kobuki.cliff) {
                state = SEARCH;
            }
            break;
						
        case OBSTACLE:
			if (stop_kobuki) {
                state=IDLE;
            }
            if (!kobuki.bumper && !kobuki.cliff) {
                state=SEARCH;
            }
            else {
                KobukiDriveToCompletion((int16_t)-80, kobuki);
                if (kobuki.cliff && !LAYOUT_3) {
                    KobukiRotateAngleToCompletion((int16_t)60*CW, kobuki);
                    KobukiDriveToCompletion((int16_t)250, kobuki);
                }
                else if (kobuki.cliff && LAYOUT_3) {
                    KobukiRotateAngleToCompletion((int16_t)100*CW, kobuki);
                    KobukiDriveToCompletion((int16_t)700, kobuki);
                    KobukiRotateAngleToCompletion((int16_t)100*CW, kobuki);
                    KobukiDriveToCompletion((int16_t)500, kobuki);
                }
                
            }		
            break;
        }
    }

}