import busio
import adafruit_pcf8523
import time
import board
from digitalio import DigitalInOut, Direction, Pull

class Clock:
    def __init__(self, time_out):
        myI2C = busio.I2C(board.SCL, board.SDA)
        self.rtc = adafruit_pcf8523.PCF8523(myI2C)
 
        self.minuteButton = DigitalInOut(board.D5)
        self.minuteButton.direction = Direction.INPUT
        self.minuteButton.pull = Pull.UP

        self.hourButton = DigitalInOut(board.D6)
        self.hourButton.direction = Direction.INPUT
        self.hourButton.pull = Pull.UP

        self.led = DigitalInOut(board.D13)
        self.led.direction = Direction.OUTPUT

        self.time_output = time_out
        
        #SetTimeToFixedValue()
    
    def SetTimeToFixedValue(self):
        #                     year, mon, date, hour, min, sec, wday, yday, isdst
        t = time.struct_time((2019,   8,   11,   21,  31,  15,    6,   -1,    -1))
        # you must set year, mon, date, hour, min, sec and weekday
        # yearday is not supported, isdst can be set but we don't do anything with it at this time
    
        print("Setting time to:", t)     # uncomment for debugging
        self.rtc.datetime = t
        print()

    def IncrementMinute(self):
        t = self.rtc.datetime
        currentMinutes = t.tm_min
        currentMinutes += 1
    
        if currentMinutes >= 60:
            currentMinutes = 0

        newT = time.struct_time((t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, currentMinutes, 0, t.tm_wday, -1, -1))
        self.rtc.datetime = newT

    def IncrementHour(self):
        t = self.rtc.datetime
        currentHour = t.tm_hour
        currentHour += 1

        if currentHour >= 24:
            currentHour = 0

        newT = time.struct_time((t.tm_year, t.tm_mon, t.tm_mday, currentHour, t.tm_min, 0, t.tm_wday, -1, -1))
        self.rtc.datetime = newT

    def OutputTimeTwelveHour(self):
        t = self.rtc.datetime
        hour = t.tm_hour
        suffix = 'AM'
        if hour > 12:
            hour -= 12
            suffix = 'PM'
        if hour == 0:
            hour = 12
        self.time_output(hour, t.tm_min, suffix)
    
    def UpdateButtons(self):
        if self.minuteButton.value:
            self.led.value = False
        else:
            self.led.value = True
            self.IncrementMinute()
    
        if self.hourButton.value:
            self.led.value = False
        else:
            self.led.value = True
            self.IncrementHour()
    
    def Update(self):
        self.OutputTimeTwelveHour()
        self.UpdateButtons()

def PrintTime(hour, minute, suffix):
        print("%d:%02d %s" % (hour, minute, suffix))

clock = Clock(PrintTime)

while True:
    clock.Update()
    time.sleep(0.2) # wait a second