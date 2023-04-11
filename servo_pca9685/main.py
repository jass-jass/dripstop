import machine, pcf8574
from machine import Pin, I2C
from servo_motor import Servos
from time import sleep


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
addr = i2c.scan()
servo = Servos(i2c, addr[0], freq=50)
while True:
    angle = int(input("angle "))
    servo.position(0, degrees = ((angle*103)/90))
