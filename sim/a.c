#include <stdint.h>

volatile uint8_t *a = (volatile uint8_t *)0x80000000;

void _start(void)
{
	static const char *text = "Hello, world!\n";

	while (1) {
		for (const char *ptr = text; *ptr; ptr++) {
			while (*(a + 1)) {
			}
			*a = *ptr;
		}
	}
}
