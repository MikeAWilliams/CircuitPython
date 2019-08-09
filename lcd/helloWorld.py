import board
from digitalio import DigitalInOut
from time import sleep
from adafruit_character_lcd.character_lcd import Character_LCD_Mono


lcd_rs = DigitalInOut(board.D13)
lcd_en = DigitalInOut(board.D12)
lcd_d4 = DigitalInOut(board.D11)
lcd_d5 = DigitalInOut(board.D10)
lcd_d6 = DigitalInOut(board.D9)
lcd_d7 = DigitalInOut(board.D6)

lcd_columns = 16
lcd_rows = 2

lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                         lcd_columns, lcd_rows)
lcd.clear()
lcd.message = "Hello\nWorld!"
sleep(4)

shifts = 10
shift_pause = 0.2
while True:
    for x in range(shifts):
        lcd.move_right()
        sleep(shift_pause)

    for x in range(shifts):
        lcd.move_left()
        sleep(shift_pause)
