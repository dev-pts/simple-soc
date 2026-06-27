#include <stdint.h>

volatile uint32_t *a = (volatile uint32_t *)0x80000000;

void _start(void)
{
	static const char *text = "Hello, world!\n";

	while (1) {
		for (const char *ptr = text; *ptr; ptr++) {
			*a = *ptr;
		}
	}
}
