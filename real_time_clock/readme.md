example using a real time clock. Adafruit PCF8523 Real Time Clock Assembled Breakout Board
Requires adafruit circuitpython bundle libraries adafruit_bus_device, adafruit_register,adafruit_pcf8523.mpy

sets up a clock where the time can be changed by an hour button and a minute button.

| clock pin | destination |
|----------:|------------:|
| gnd       | ground      |
| vcc       | 3 volts     |
| sda       | feather sda |
| scl       | feather scl |
| sqw       | blank       |

| second button | destination |
|--------------:|------------:|
| top left      | feather D5  |
| top right     | blank       |
| bootom left   | blank       |
| bottom right  | gnd         |


| hour button   | destination |
|--------------:|------------:|
| top left      | feather D6  |
| top right     | blank       |
| bootom left   | blank       |
| bottom right  | gnd         |


| feather pin   | destination |
|--------------:|------------:|
| 3v            | 3v bus      |
| gnd           | gnd bus     |
| d6            | hour tl     |
| d5            | minute tl   |
| scl           | clock scl   |
| sda           | clock sda   !
