#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <irq.h>
#include <uart.h>
#include <time.h>
#include <generated/csr.h>

void sleep(void);

int s = 0;

void sleep(void) {
  while(1) {
    if(elapsed(&s, SYSTEM_CLOCK_FREQUENCY)) {
      break;
    }
  }
}

int main(void) {
  irq_setmask(0);
  irq_setie(1);
  uart_init();
  time_init();

  elapsed(&s, -1);

  puts("LED CPU booting...\n");

  while (true) {
    blinker_leds_out_write(0);
    sleep();
    if (blinker_switches_in_read()) {
      blinker_leds_out_write(1);
      sleep();
    }
  }

  return 0;
}
