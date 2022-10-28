/*
 *
 *  =========================
 * |     MCP Assignment 3     |
 * | Michael Laden - a1748876 |
 * | Michael Neill - a1764673 |
 *  =========================
 *
 * File:          adc.c
 * Description:   Enable the microcontroller to initialise and read from the ADC from the selected channel. 
 */

#include "adc.h"
#include "LPC407x_8x_177x_8x.h"

void ADCInit ( void ) {

	/*
	PCADC (A/D converter (ADC) power/clock control bit.) | PCGPIO (Power/clock control bit for IOCON, GPIO, and GPIO interrupts.). 

	From pg. 29 - 30 UM
	*/

	LPC_SC -> PCONP |= ((1 << 12) | (1 << 15)) ; 

	/*
	LPC_ADC -> CR = (( ?? << 1) | // SEL - Select pin (s) (0..7) to be sampled and collected
					 ( ?? << 8) | // CLKDIV - The APB clock is 60 MHz and we want < 12.4 MHz
					 ( ?? << 21)); // PDN - ADC is operational

	From pg. 805 UM: Set-up the ADC using the Control Register (CR) - AD0CR
	*/

	LPC_ADC -> CR = (1 << 1) | (4 << 8) |(1 << 21);
}

uint32_t ADCRead(uint8_t channel) {

	// Stop conversions running on the ADC. From pg. 805 UM.
	LPC_ADC -> CR &= ~(7 << 24); 

	// START - Start conversion now. Table 678 from pg. 805 UM.
	LPC_ADC -> CR |= ( 1 << 24) ; 

	//Table 677 on pg. 804 UM. DR1 ref. Table 681 on pg. 808 UM, the DONE flag is stored in the 31st bit. 
	while ( !(LPC_ADC->DR[channel] & (1U << 31)) ); 
	
	// Stop conversions running on the ADC. From pg. 805 UM.
	LPC_ADC -> CR &= ~(7 << 24 );
	
	/* Get the value returned by the ADC0 .0 channel
	Right shift by four bits, then mask the RESULT data from the first twelve bit. */
	uint32_t data = ( ( LPC_ADC -> DR[channel] >> 4 ) ) & 0xFFF; 
	return data;

}
