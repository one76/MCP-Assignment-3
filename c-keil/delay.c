#include "delay.h"

void DelayMs(uint32_t ms) {
  ms *= (SystemCoreClock/10000);
  while (ms--) { __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); __NOP(); }
}
