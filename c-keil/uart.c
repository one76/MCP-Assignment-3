/*
*
*  =========================
* |     MCP Assignment 3     |
* | Michael Laden - a1748876 |
* | Michael Neill - a1764673 |
*  =========================
*
* File:             uart.c
* Description:      UART serial communication functions.
*                   Implementation file
* 
*/


// ==== INCLUDES ====
#include "uart.h"
#include "LPC407x_8x_177x_8x.h" // Hack solution
// ==== INCLUDES ====


// ==== MACROS ====
#define PCUART_0 3
#define PCUART_2 24
#define PCUART_3 25

#define KOBOUKI_TX_UART_0 (0 << 16)| 0
#define KOBOUKI_RX_UART_0 (0 << 16)| 1
// ==== MACROS ====


// ===== FUNCTION IMPLEMENTATIONS ====
void UARTInit(void) {
	
	// 1) turn on the power
	LPC_SC -> PCONP |= (1U << PCUART_0); //UART0 power/clock control bit
	
	// 2) check peripheral clock
	volatile int CCLK = SystemCoreClock;
	volatile int PCLK = PeripheralClock;
	
	// 3) baud rate
	// options to set divisor and 115200 baud (116220 actual)
    LPC_UART0 ->LCR =   (1U << 7) ; // DLAB - enable divisor latches. Table 401
    LPC_UART0 ->DLL =   0x16; // DLLSB - Divisor latch LSB register
    LPC_UART0 ->DLM =   0x0; // DLMSB - Divisor latch MSB register
    LPC_UART0 ->FDR =   (0x7 << 0) | // DIDADDVAL - baud rate prescaler divisor
                        (0xF << 4) ; // MULVAL - bad rate prescaler multiplier
    LPC_UART0 ->LCR &=  ~(1U << 7) ; // DLAB - disable divisor latches (why? to enable UART interrupts?)
	
	// 4) FIFO
	LPC_UART0 -> FCR = (1U << 0) | (1U << 1) | (1U << 2);
	
	// 5) Select pins and pin modes
	GPIOPinConfig(KOBOUKI_TX_UART_0 , 0x4 | 0x2 << 3); // MODE - IOCON register bit description
	GPIOPinConfig(KOBOUKI_RX_UART_0 , 0x4 | 0x2 << 3); // MODE - IOCON register bit description
	
	// 6) Configure UART
    LPC_UART0 -> LCR |= (0x3 << 0);
	
	// 7) Enable Tx
	LPC_UART0 -> TER = (1U << 7); //TXEN - send data when enabled
}

void UARTTx(uint8_t byte) {
    // hold until FIFO is empty - auto cleared
    while( !(LPC_UART0 -> LSR & (1U << 5) ) ); // THRE - transmitter holding register empty
    
    // write FIFO
    LPC_UART0 -> THR = byte; // THR - transmit holding register
}

uint8_t UARTRx(void) {
    // hold when an unread character in FIFO - auto cleared
    while( !(LPC_UART0 -> LSR & 1U) ); // RDR - check if FIFO empty. Table 402 PAge 503

    // read FIFO
    return (LPC_UART0 -> RBR & 0xFF); //RBR - reciever buffer register
                                    // oldest recieved byte in FIFO. Table 393 Page 496
}
// ===== FUNCTION IMPLEMENTATIONS ====
