#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <irq.h>
#include <uart.h>
#include <time.h>
#include <generated/csr.h>
#include <generated/mem.h>
#include <hw/flags.h>
#include <console.h>
#include <system.h>

int main(void)
{
	irq_setmask(0);
	irq_setie(1);
	uart_init();

	puts("Demo firmware booting...\r\n");

	time_init();

        while (1);

	return 0;
}
