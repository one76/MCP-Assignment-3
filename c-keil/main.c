/* 
* 
*  ===========================
* |       MCP Assignment 3     |
* |   Michael Laden - a1748876 | 
* |   Michael Neill - a1764673 |
*  ========================== 
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
enum {IDLE, SEARCH, FIND, OBJECT, OBSTACLE} state;

int main() {
    Kobuki_Typedef kobuki   = {}
    US_Typedef object       = {}
    int collected_rocks[2] = {0,0};
    uint16_t old_range;
    int DIR = CCW;


    ADC_Init();
    UART_Init();
    Ultrasoic_Init();


    while(1) {
        
        // Update Sensor Values
        Kobuki_Read(&kobuki);
        Ultrasonic_Detect(&object);
        
        // Boolean Values to Increase Readablility
        int STOP_KOBUKI = (
                kobuki.button == BUTTON_1   ||
                kobuki.wheeldrop            ||
                kobuki.bumper               ||
                kobuki.cliff                ||
            );
        int COLLECTING_FIRST_ROCK = collected_rocks[0] == FALSE
        int FOUND_NEW_ROCK =  !(old_range-8 <= object.range || old_range+8 >= object.range)
        int KEEP_SEARCHING = !COLLECTING_FIRST_ROCK || (COLLECTING_FIRST_ROCK && object.range<850) ? FALSE : TRUE

        switch (state)
        {
        case IDLE:
            if (kobuki.btton == BUTTON_0)
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
                state = FIND;
            }
            else if (kobuki.bumper || kobuki.cliff) {
                state = OBSTACLE;
            }
            else if (!object.detected || (object.detected && KEEP_SEARCHING)) {
                Kobuki_Rotate(SEARCH_SPEED*DIR)
            }
            break;
        case FIND:
            break;
        case OBJECT:
            break;
        case OBSTACLE:
            break;
        }
    }
        
}