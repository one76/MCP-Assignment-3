#ifndef PIN_DEFS_H
#define PIN_DEFS_H

// Define peripherals to be used on LPC4088 QSB & Exper BB

// We use the structure: (port << 16) | pin

// QSB LEDs
#define LED_1 (1 << 16) | 18 // Px_xx
#define LED_2 (0 << 16) | 13 // Px_xx
#define LED_3 (1 << 16) | 13 // Px_xx
#define LED_4 (2 << 16) | 19 // Px_xx

//// BB Joystick
#define JOY_LT (5 << 16) | 0 // Px_xx
#define JOY_RT (5 << 16) | 4 // Px_xx
#define JOY_UP (5 << 16) | 2 // Px_xx
#define JOY_DN (5 << 16) | 1 // Px_xx
#define JOY_CR (5 << 16) | 3 // Px_xx

// Define motor pins.
#define MOTOR_A1 (1 << 16) | 24
#define MOTOR_A3 (1 << 16) | 23
#define MOTOR_B1 (1 << 16) | 20
#define MOTOR_B3 (0 << 16) | 21

// Define potentiometer pins.
#define POT_RT_ADC_0 (0 << 16) | 23

// Define ultrasonic ADC pin and channel
#define ULTRASONIC_ADC_1 (0 << 16) | 24 // Page 139 and LPC4088 Experiment BB Circuit Diagrams ADC0_IN[1]
#define ULTRASONIC_CHANNEL 1

#endif
