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

class RGB:
    def __init__(self, re, gr, bl):
        self.r = re
        self.g = gr
        self.b = bl

class RGBArrayDiscrete:
    def __init__(self, rgbArray):
        self.rgbArray = rgbArray
        self.index = 0
        self.direction = 1
    
    def Update(self):
        self.index += self.direction
        if self.index >= (len(self.rgbArray) - 1) or self.index <= 0:
            self.direction *= -1
    
    @property
    def rgb(self):
        return self.rgbArray[self.index]

    @property
    def r(self):
        return self.rgb.r

    @property
    def g(self):
        return self.rgb.g
    
    @property
    def b(self):
        return self.rgb.b

def GetRainbowRGB():
    result = []
    result.append(RGB(148,0,211))
    result.append(RGB(75,0,130))
    result.append(RGB(0,0,255))
    result.append(RGB(0,255,0))
    result.append(RGB(255,255,0))
    result.append(RGB(255,127,0))
    result.append(RGB(255,0,0))
    return result

def GetRainbowNoRedRGB():
    result = []
    result.append(RGB(148,0,211))
    result.append(RGB(75,0,130))
    result.append(RGB(0,0,255))
    result.append(RGB(0,255,0))
    result.append(RGB(255,255,0))
    result.append(RGB(255,127,0))
    return result

def Interpolate(n, np, number, index):
    return n + (np - n) / number * index

def AddColorsBetween(colors, numberToAdd):
    lastColor = colors[0]
    result = []
    iterColor = iter(colors)
    next(iterColor)
    for color in iterColor:
        for i in range(numberToAdd):
            indexR = Interpolate(lastColor.r, color.r, numberToAdd, i)
            indexG = Interpolate(lastColor.g, color.g, numberToAdd, i)
            indexB = Interpolate(lastColor.b, color.b, numberToAdd, i)
            result.append(RGB(indexR, indexG, indexB))
        lastColor = color
    result.append(colors[len(colors) - 1])
    return result


led = ComonAnaodeLED(rpin = board.D13, gpin = board.D12, bpin = board.D11)
color = RGBArrayDiscrete(AddColorsBetween(GetRainbowNoRedRGB(), 10))

while True:
    led.SetRGB(color.r, color.g, color.b)
    color.Update()
    time.sleep(0.1)