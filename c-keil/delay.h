#ifndef DELAY_H
#define DELAY_H

#include <stdint.h>
#include "LPC407x_8x_177x_8x.h"
#include "system_LPC407x_8x_177x_8x.h"

// We have taken this private function from
// "system_LPC407x_8x_177x_8x.c"
/**
	* @brief delay in ms
	* @param ms
	* @return none
*/

void DelayMs(uint32_t ms);

#endif
