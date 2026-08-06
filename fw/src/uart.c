#include <stdint.h>
#include <stdio.h>

#define UART_BASE 0x80000000

static uint8_t readb(uintptr_t addr)
{
	return *((volatile uint8_t *)addr);
}

static void writeb(uint8_t b, uintptr_t addr)
{
	*((volatile uint8_t *)addr) = b;
}

static int sample_putc(char c, FILE *file)
{
	(void)file;

	if (c == '\n') {
		sample_putc('\r', file);
	}

	while (readb(UART_BASE + 1)) {
	}

	writeb(c, UART_BASE);
	return c;
}

static FILE __stdio = FDEV_SETUP_STREAM(
	sample_putc,
	NULL,
	NULL,
	_FDEV_SETUP_WRITE
);

FILE *const stdout = &__stdio;
FILE *const stderr = &__stdio;
