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


# Module that turns an LED on and off at some interval (`period` clock cycles),
# with a specific on time (`width` clock cycles).
# i.e. `width/period` is the PWM duty cycle, and `1/period` is the PWM frequency.
#     ________                       ________
# ___|        |_____________________|        |_____________________
#    <-width->
#    <------------period----------->
class BlinkerPwm(Module):
  def __init__(self, led, width, period):
    # Create a counter to track where we are in the pulse.
    counter = Signal(max=period)

    self.comb += [
      # On until we get to `width`
      If(counter < width,
        led.eq(1)
      ).Else(
        led.eq(0)
      ),
    ]
    self.sync += [
      If(counter == period - 1,
        # Reset the counter when we get to `period-1`
        counter.eq(0)
      ).Else(
        # Otherwise increment the counter.
        counter.eq(counter + 1)
      )
    ]


class Blinker(Module):
  def __init__(self, platform, *args, **kwargs):
    led1 = platform.request('user_led')
    self.submodules.blinker = BlinkerFlash(led1, cycles=int(1e9 / platform.default_clk_period))

    led2 = platform.request('user_led')
    self.submodules.pwm = BlinkerPwm(led2, width=1000, period=30000)

    # Wire up the red leds to the switches, and green leds to the buttons.
    rgb = platform.request("rgb_leds")
    for i in range(4):
      self.comb += [
        rgb.r[i].eq(platform.request('user_sw')),
        rgb.g[i].eq(platform.request('user_btn'))
      ]


SoC = Blinker
