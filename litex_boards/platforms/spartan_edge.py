# Spartan Edge Accel:
# https://github.com/SeeedDocument/Spartan-Edge-Accelerator-Board

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("clk100", 0, Pins("H4"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("J1"),   IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("A13"),  IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("M10")),
        Subsignal("rx", Pins("N10")),
        IOStandard("LVCMOS33")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = []

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7s15ftgb196-1", _io, _connectors, toolchain="vivado")

    def create_programmer(self):
        return OpenOCD("openocd_xc7_ft232r.cfg")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/100e6)
