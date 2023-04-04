from machine import Pin
from time import sleep
import servo


servo = servo.Servo(4)

while True:
    angle = int(input('angle '))
    servo.write(angle)
