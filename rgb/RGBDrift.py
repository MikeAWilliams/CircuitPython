import time
import board
from analogio import AnalogOut
import pulseio

def ConvertByteTo16BitInverted(byte_color):
    return int((255 - byte_color) / 255 * 0xffff)

class ComonAnaodeLED:
    def __init__(self, rpin, gpin, bpin):
        red_cycle = 0xffff 
        green_cycle = 0xffff 
        blue_cycle = 0 
        self.red = pulseio.PWMOut(rpin, duty_cycle=red_cycle)
        self.green = pulseio.PWMOut(gpin, duty_cycle=green_cycle)
        self.blue = pulseio.PWMOut(bpin, duty_cycle=blue_cycle)

    def SetRGB(self, r, g, b):
        self.red.duty_cycle = ConvertByteTo16BitInverted(r)
        self.green.duty_cycle = ConvertByteTo16BitInverted(g)
        self.blue.duty_cycle = ConvertByteTo16BitInverted(b)

class MovingByteValue:
    def __init__(self, val, delta):
        self.value = val
        self.delta = delta
    
    def Update(self):
        self.value += self.delta
        if self.value >= 255 or self.value <= 0:
            self.delta *= -1

class MovingRGB:
    def __init__(self, r, g, b, rdelta, gdelta, bdelta):
        self.rmover = MovingByteValue(r, rdelta)
        self.gmover = MovingByteValue(g, gdelta)
        self.bmover = MovingByteValue(b, bdelta)
    
    def Update(self):
        self.rmover.Update()
        self.gmover.Update()
        self.bmover.Update()
    
    @property
    def r(self):
        return self.rmover.value

    @property
    def g(self):
        return self.gmover.value
    
    @property
    def b(self):
        return self.bmover.value

led = ComonAnaodeLED(rpin = board.D13, gpin = board.D12, bpin = board.D11)
color = MovingRGB(254, 1, 127, -1, 1, -1)

while True:
    led.SetRGB(color.r, color.g, color.b)
    color.Update()
    time.sleep(0.03)