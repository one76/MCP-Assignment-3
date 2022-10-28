/* ADC_Init - Initialise the ADC0 of LPC4088
ADC_Read - Start ADC conversion and read a value from the initialised channel (s)
A basic configuration checklist can be found on pg. 802 user manual (UM) 10562
*/

#include "adc.h"
#include "LPC407x_8x_177x_8x.h" // Hack Solution



void ADC_Init ( void ) {
	// pg. 29 - 30 UM
	// Turn on the power / clock to our ADC via the PCONP register
	// Additionally , we ensure the power / clock is set for the IOCON & GPIO ( reset 1)
	LPC_SC -> PCONP |= ( (1 << 12) | (1 << 15) ) ; // PCADC | PCGPIO
	
	// pg. 805 UM
	// Set-up the ADC using the Control Register (CR) - AD0CR
	/*
		LPC_ADC -> CR = ( ?? << 0) | // SEL - Select pin (s) (0..7) to be sampled and collected
									 ( ?? << 8) | // CLKDIV - The APB clock is 60 MHz and we want < 12.4 MHz
									 ( ?? << 21); // PDN - ADC is operational
	*/
	LPC_ADC -> CR = (1 << 1) |(4 << 8) |(1 << 21);

	// pg. 138 - 139 UM
	// Set the functionality of the pin to ADC in the IOCON register
	// Select analogue mode - there is a macro for this in the header file
	// GPIO_Pin_Config(POT_RT_ADC_0 , 0x01 | // FUNCT - IOCON control register
	//									IOCON_ANALOG_MODE); // ADMODE - IOCON register bit description
}

uint32_t ADC_Read(uint8_t channel) {
	// pg. 805 UM
	// Stop any conversion running on the ADC
	LPC_ADC -> CR &= ~(7 << 24); // START - No Start
	// Start the ADC conversion
	LPC_ADC -> CR |= ( 1 << 24) ; // START - Start conversion now !!! HURRY !!
	
	// pg. 804 & 806 UM
	// Wait until the ADC conversion completes by looking at the Data Register (DR)
	while ( !(LPC_ADC->DR[channel] & (1U << 31)) ); // DONE - wait until complete
	
	// pg. 805 UM
	// Stop any conversion running on the ADC
	LPC_ADC -> CR &= ~(7 << 24 ); // START - No Start
	
	// pg. 804 & 806 UM
	// Get the value returned by the ADC0 .0 channel
	uint32_t data = ( ( LPC_ADC -> DR[channel] >> 4 ) ) & 0xFFF; // RESULT - The 12 - bit digital value
	return data ;
}
