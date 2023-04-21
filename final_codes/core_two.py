from machine import Pin, Timer, I2C
import time
from hx711 import HX711
from servo_motor import Servos



######## Initialization of pins ########
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))
addr = i2c_device.scan()
# Inputs
load_cell = HX711(d_out = 16, pd_sck = 17, channel = 3)
# Outputs
buzzer = Pin(18, Pin.OUT)
servo = Servos(i2c_device, addr[2], freq=50)

### Variables for pin status of pins ###
# shared for both core functions
calibrate_load = 0
volume = 500
volume_left = 500

######## Timer Interrupt handler #######
def ISR_Timer(arg):
    timer_10_sec.deinit()      # turn off timer
    servo.position(0, 90)           # 85 degrees
    buzzer.off()        # turn off buzzer



### Interrupt handler for 10% weight ###
def ISR_10_percent():
    timer_10_sec = Timer(1)
    timer_10_sec.init(period = 10000, mode = Timer.ONE_SHOT, callback = ISR_Timer)
    buzzer.on()


def calibrate():
    weight = 0
    buzzer.on()
    time.sleep(0.2)
    buzzer.off()
    time.sleep(1)
    for i in range(150):
        if load_cell.is_ready:
            raw_weight = load_cell.read(raw = False)
            weight = weight + 1*((raw_weight+81752.99)/217.3966)
    return weight / 150


def critical_core():
    global calibrate_load
    global volume
    global volume_left
    weight_ref = 0
    while True:
        if calibrate_load:
            weight_ref = calibrate() - volume
            calibrate_load = 0
        weight = 0
        for i in range(50):
            if load_cell.is_ready:
                raw_weight = load_cell.read(raw = False)
                weight = weight + 1*((raw_weight+81752.99)/217.3966)
        weight = weight / 50
        volume_left = weight - weight_ref
        if volume_left/volume < 0.1:
            ISR_10_percent()
