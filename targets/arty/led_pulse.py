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


# Module that pulses an LED by ramping its brightness.
# Every `cycles` clock cycles, the PWM width is increased, up to 100%.
class BlinkerPulse(Module):
  def __init__(self, led, period, cycles):
    # Create a counter to track where we are in the pulse.
    counter_pwm = Signal(max=period)
    # Create a counter to track cycles until we increment brightness.
    counter_brightness = Signal(max=cycles)
    # Rather than a fixed width, use a signal to allow it to increment.
    width = Signal(max=period)

    # Brightness / PWM:
    self.comb += [
      # On until we get to `width`
      If(counter_pwm < width,
        led.eq(1)
      ).Else(
        led.eq(0)
      )
    ]
    self.sync += [
      If(counter_pwm == period - 1,
        # Reset the PWM counter when we get to `period-1`
        counter_pwm.eq(0)
      ).Else(
        # Otherwise increment the PWM counter.
        counter_pwm.eq(counter_pwm + 1)
      )
    ]

    # Pulsing:
    self.sync += [
      If(counter_brightness == 0,
        # Increment the brightness.
        width.eq(width + 1),
        # Start counting backwards from `cycles` again.
        counter_brightness.eq(cycles - 1)
      ).Else(
        # Keep counting backwards...
        counter_brightness.eq(counter_brightness - 1)
      ),
      If(width == period - 1,
        # When we get to full brightness, reset back to zero.
        width.eq(0)
      )
    ]


class Blinker(Module):
  def __init__(self, platform, *args, **kwargs):
    led1 = platform.request('user_led')
    self.submodules.blinker = BlinkerFlash(led1, cycles=int(1e9 / platform.default_clk_period))

    led2 = platform.request('user_led')
    self.submodules.pwm = BlinkerPwm(led2, width=1000, period=30000)

    led3 = platform.request('user_led')
    self.submodules.pulse = BlinkerPulse(led3, period=30000, cycles=int(1e9 / platform.default_clk_period / 30000))

    # Wire up the red leds to the switches, and green leds to the buttons.
    rgb = platform.request("rgb_leds")
    for i in range(4):
      self.comb += [
        rgb.r[i].eq(platform.request('user_sw')),
        rgb.g[i].eq(platform.request('user_btn'))
      ]


SoC = Blinker
