/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             kobuki.c
* Description:      Kobuki functions for transferring and receiving information 
*                   from and to the kobuki. Also, functions for controlling the
*                   kobuki. Implementation file.
* 
*/


// ==== INCLUDES ====
#include <math.h>
#include <stdlib.h>

#include "gpio.h"
#include "uart.h"
#include "kobuki.h"
// ==== INCLUDES ====


// ==== MACROS ====
// Define buffer for feedback
#define SIZE_FEEDBACK   26

// Buffer defintions for payload
#define BUMPER      4
#define WHEEL_DROP  5
#define CLIFF       6
#define BUTTON      13

#define DIST_LSB    7
#define DIST_MSB    8
#define ANGLE_LSB   24
#define ANGLE_MSB   25

#define ROTATE      0
#define DRIVE       1

#define EXTERN_PWR  0x30

#define PI                      3.1416f
#define WHEEL_RADIUS            35                  // mm
#define REVOLUTIONS_PER_TICK    (132.0f/6545.0f*52)
#define MM_PER_TICK             0.08529209
#define DEG_PER_TICK            ((float) 1/100)

#define MIN_SPEED               (int16_t)50         // mm/s
#define GAIN_ROTATE             ((float)100/45)		// Want the Kobuki to start slowing down at 45 deg
#define GAIN_DRIVE	            ((float)100/100) 	// Want the Kobuki to start slowing down at 100 mm

#define sign(x) (int8_t) (signbit ( x ) ? -1 : 1)
// ==== MACROS ====


// ==== FUNCTION IMPLEMENTATIONS ====
uint8_t KobukiRx(uint8_t *feedback , uint32_t size_feedback) {

    uint8_t feedback_header = 0, size_payload = 0, checksum = 1, rx_checksum = 0, i;

    // wait for start of data stream - header 0
    while (feedback_header != 0xAA ) {
        feedback_header = UARTRx();
    }

    // check for header 1 as next byte
    feedback_header = UARTRx();

    if(feedback_header == 0x55 ) {
        // reset checksum
        checksum = 0;

        // first byte is size of payload in bytes
        size_payload = UARTRx();

        // checksum is XOR�ed value of entire bytestream
        checksum ^= size_payload;

        // size of basic sensor data
        for(i = 0; i < size_feedback; i++) {
            feedback[i] = UARTRx();
            checksum ^= feedback[i];
        }

        // size of rest of byestream - not required , just for checksum
        for(i = size_feedback; i < size_payload; i++) {
            checksum ^= UARTRx ();
        }

        // checksum from kobuki - final byte
        rx_checksum ^= UARTRx ();
    }

    // checksums equal
    if (checksum == rx_checksum){
        return 0;
    }

    // checksums do not equal
    else {
        return 1;
    }
}


// kobuki read datastream
void KobukiRead(Kobuki_Typedef *kobuki) {
    
    // Init buffer & checksum
    uint8_t kobuki_rx_buffer[SIZE_FEEDBACK ];
    uint8_t checksum_result;

    // Read kobuki Tx data stream
    checksum_result = KobukiRx(kobuki_rx_buffer ,SIZE_FEEDBACK);

		kobuki -> distance_complete = distance_complete;
		kobuki -> rotation_complete = rotation_complete;
	
    // If checksum �checks out �, update sensor variables from buffer
    if (checksum_result == 0) {
        kobuki -> bumper = kobuki_rx_buffer[BUMPER ];
        kobuki -> wheeldrop = kobuki_rx_buffer[WHEEL_DROP ];
        kobuki -> cliff = kobuki_rx_buffer[CLIFF];
        kobuki -> button = kobuki_rx_buffer[BUTTON ];
				
				kobuki -> distance = (kobuki_rx_buffer[DIST_MSB] << 8) |  kobuki_rx_buffer[DIST_LSB];
				kobuki -> angle = (kobuki_rx_buffer[ANGLE_MSB] << 8) | kobuki_rx_buffer[ANGLE_LSB];
    }

    // otherwise do not update
    else {}
}

void KobukiTx(uint8_t *payload, uint8_t size_payload) {
    uint8_t checksum = 0, i;
    UART_Tx( 0xAA ); // Send header 0
    UART_Tx( 0x55 ); // Send header 1
    UART_Tx( size_payload ); // Send size of payload in bytes
    
    checksum ^= size_payload; // Calcualate running checksum
    
    // Send each byte of payload one-by-one
    for(i = 0; i < size_payload; i++) {
        UART_Tx( payload[i] );
        checksum ^= payload[i];
    }

    UART_Tx(checksum); // Send checksum
}

void KobukiRotateOrDrive(int16_t speed, int mode) {
    // Saturation to avoid going over speed limit
    if ( speed > SPEED_LIMIT ) { 
        speed = SPEED_LIMIT;
    }
    else if ( speed < -SPEED_LIMIT ) {
        speed = (~SPEED_LIMIT)+1; // speed = -SPEED_LIMIT
    }

    // Split LSB & MSB for payload
    uint8_t speed_lsb = (speed & 0x00FF); 
    uint8_t speed_msb = (speed & 0xFF00) >> 8;

    uint8_t radius_lsb, radius_msb = 0x00;

    if (mode == ROTATE) {
        radius_lsb = 0x01;
    }
    else if (mode == DRIVE) {
        radius_lsb = 0x00;
    }

    // Kobuki Serial Bytestream pdf Page 5
    uint8_t payload[6]  = {0x01,0x04,speed_lsb,speed_msb,radius_lsb,radius_msb};

    KobukiTx(payload , 6); 
}

void KobukiRotate(int16_t speed) {
    // Rotation is CCW
    KobukiRotateOrDrive(speed, ROTATE);
}
void Kobuki_Drive(int16_t speed) {
    KobukiRotateOrDrive(speed, DRIVE);
}

void KobukiUpdateLEDs(int8_t led_1_colour, int8_t led_2_colour) {
    // Split LSB & MSB for payload
    uint8_t GPO_lsb = EXTERN_PWR; //keep 5V AND 3.3V on
    uint8_t GPO_msb = (led_1_colour | led_2_colour << 8);

    uint8_t payload[4] = {0x0C, 0x02, GPO_lsb, GPO_msb}; // Page 6 - 7 of Kobuki Serial Bytestream

    KobukiTx(payload ,sizeof(payload));
}

void KobukiDriveDistanceSetpoint(uint16_t current_distance_tick, int16_t distance) {
		distance_complete = 0;
		setpoint_distance_tick = current_distance_tick + (int32_t)(distance/MM_PER_TICK);
}

void KobukiDriveDistance (uint16_t current_distance_tick) {
		int16_t speed;
		int16_t error;
		uint16_t setpoint_alias;
	
		error = (setpoint_distance_tick - current_distance_tick) * MM_PER_TICK;
		setpoint_alias = ( (setpoint_distance_tick + 0x10000) % 0x10000);
	
		if ( 	((setpoint_distance_tick > 0xFFFF) 	&& (current_distance_tick < setpoint_alias)) || 
					((setpoint_distance_tick < 0) 			&& (current_distance_tick > setpoint_alias)) 	) {
				error = (setpoint_alias - current_distance_tick) * MM_PER_TICK;
		}
		if ( abs(error) <= 2 ) {
				distance_complete = 1;
				KobukiDrive(STOP);
		}
		else {
				speed = (sign(error) * MIN_SPEED) + (GAIN_DRIVE * error);
				KobukiDrive(speed);
		}
}

void KobukiDriveToCompletion(int16_t distance, Kobuki_Typedef kobuki) {
	KobukiDriveDistanceSetpoint(kobuki.distance, distance);
	while (kobuki.distance_complete == 0) {
		KobukiRead(&kobuki);
		KobukiDriveDistance(kobuki.distance);
	}
}

void KobukiRotateAngleSetpoint(int16_t current_angle_tick, int16_t rot_angle_deg) {
		int32_t init_angle;
		rotation_complete = 0;
		init_angle = (current_angle_tick + (int32_t)18000) * DEG_PER_TICK;
		setpoint_angle_deg = (init_angle + rot_angle_deg + 360) % 360;
}

void KobukiRotateAngle(int16_t current_angle_tick) {
		int16_t speed;
		int16_t error;
		int32_t current_angle_deg;
	
		current_angle_deg = (current_angle_tick + (int32_t)18000)*DEG_PER_TICK;
		error = (setpoint_angle_deg - current_angle_deg);
		
		if (abs(error) > 180) {
				error = -sign(error)*(abs(error) % 180);
		
				if ( (error < 0) && (current_angle_deg < setpoint_angle_deg) ) {
						error = -(error + 180);
				}
				else if ( (error > 0) && (current_angle_deg > setpoint_angle_deg) ) {
						error = -(error - 180);
				}
		}
		if (abs(error) <= 5) {
				rotation_complete = 1;
				KobukiRotate(STOP);
		}
		else {
				speed = (sign(error) * MIN_SPEED) + (GAIN_ROTATE * error);
				KobukiRotate(speed);
		}
}

void KobukiRotateAngleToCompletion(int16_t rot_angle_deg, Kobuki_Typedef kobuki) {
	KobukiRotateAngleSetpoint(kobuki.angle, rot_angle_deg);
	int EXIT_COUNTER = 200;
	while (kobuki.rotation_complete == 0 && EXIT_COUNTER-->=0) {
		KobukiRead(&kobuki);
		KobukiRotateAngle(kobuki.angle);
	}
}
// ==== FUNCTION IMPLEMENTATIONS ====
