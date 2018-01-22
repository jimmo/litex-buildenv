from litex.soc.interconnect.csr import AutoCSR
from litex.soc.cores.gpio import GPIOOut
from litex.gen import *
from targets.arty.base import BaseSoC
from targets.utils import csr_map_update


class BlinkerCPU(AutoCSR, Module):
  def __init__(self, led):
    self.submodules.leds = GPIOOut(led)


class BlinkSoC(BaseSoC):
  csr_peripherals = ('blinker',)
  csr_map_update(BaseSoC.csr_map, csr_peripherals)

  def __init__(self, platform, *args, **kwargs):
    BaseSoC.__init__(self, platform, *args, **kwargs)
    led = platform.request('user_led')
    self.submodules.blinker = BlinkerCPU(led)


SoC = BlinkSoC
