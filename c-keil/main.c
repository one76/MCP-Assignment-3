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

// STATES
enum {IDLE, SEARCH, FIND, OBJECT, OBSTACLE} state;

int main() {
    Kobuki_Typedef kobuki   = {}
    US_Typedef object       = {}

    ADC_Init();
    UART_Init();
    Ultrasoic_Init();

    while(1) {
        
        Kobuki_Read(&kobuki);
        Ultrasonic_Detect(&object);
        
        switch (state)
        {
        case IDLE:
            break;
        case SEARCH:
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