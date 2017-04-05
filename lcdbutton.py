import lcddriver
import datetime
import RPi.GPIO as GPIO
import time

display = lcddriver.lcd()
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        display.lcd_clear()
        display.lcd_display_string("Button Pressed", 1)
        display.lcd_display_string(str(datetime.datetime.now()), 2)
        
    	time.sleep(0.2)
