import time
import board
import digitalio
import random

port = board.GP25
led = digitalio.DigitalInOut(port)
led.direction = digitalio.Direction.OUTPUT

# RIP.I will make the LED blink for the same number of years my grandmother lived.
num = 0
while (num <= 102):
    print("LED ON")
    led.value = True
    time.sleep(random.random())
    print("LED OFF")
    led.value = False
    time.sleep(0.1)
    num += 1
    print(num)
print("Please rest peacefully in heaven.")
