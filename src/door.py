import pigpio
import time


# set pins
default_pins = {
    'motion': 3, #read data
    'motion_led': 4, #output high
    'door_in': 20, #read data
    'door_out': 21, #output high power
}

class DoorControl():
    def __init__(self, pins = default_pins):
        # initialize pigpio
        self.pi = pigpio.pi()
        self.pins = pins

    def setupPins(self):
        self.pi.set_mode(sensor[3], pigpio.INPUT)
        self.pi.set_pull_up_down(sensor[3], pigpio.PUD_DOWN)
        self.pi.set_mode(output[4], pigpio.OUTPUT)

        self.pi.set_mode(sensor[20], pigpio.INPUT)
        self.pi.set_pull_up_down(sensor[20], pigpio.PUD_DOWN)
        self.pi.set_mode(output[21], pigpio.OUTPUT)
