from litex.gen import *


# Module that toggles an LED every `cycles` clock cycles.
class BlinkerFlash(Module):
  def __init__(self, led, cycles):
    # Create a counter that can hold a value at least as big as `cycles`.
    counter = Signal(max=cycles)

    # Every time the counter gets to zero, toggle the LED.
    self.sync += [
      If(counter == 0,
         # Reset the counter back to `cycles`.
         counter.eq(cycles - 1),
         # Toggle LED.
         led.eq(~led),
      ).Else(
        # Otherwise (i.e. most of the time) -- decrement the counter.
	counter.eq(counter - 1),
      ),
    ]


class Blinker(Module):
  def __init__(self, platform, *args, **kwargs):
    led1 = platform.request('user_led')
    self.submodules.blinker = BlinkerFlash(led1, cycles=int(1e9 / platform.default_clk_period))

    # Wire up the red leds to the switches, and green leds to the buttons.
    rgb = platform.request("rgb_leds")
    for i in range(4):
      self.comb += [
        rgb.r[i].eq(platform.request('user_sw')),
        rgb.g[i].eq(platform.request('user_btn'))
      ]


SoC = Blinker
