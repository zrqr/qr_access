import gpiod
import sys
import time

CHIP = "/dev/gpiochip1"
GATE_LINE_OFFSET = 91

class GateRelay():
    def __init__(self):
        self.chip = gpiod.chip(CHIP)
        self.gate_pin = self.chip.get_line(GATE_LINE_OFFSET)
     
        config = gpiod.line_request()
        config.consumer = "Blink"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT

        self.gate_pin.request(config)

        self.gate_pin.set_value(0)

    def open(self):

        self.gate_pin.set_value(1)
        time.sleep(0.7)
        self.gate_pin.set_value(0)