from machine import Pin, I2C
from servo_motor import Servos

i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))
addr = i2c_device.scan()
servo = Servos(i2c_device, addr[2], freq=200)

angle = 0
while angle>=0:
    angle = int(input("angle "))
    servo.position(0, angle)