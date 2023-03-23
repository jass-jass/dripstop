### import ###
from machine import Pin, PWM, I2C
from micropython import const
from time import sleep
import uasyncio
from hx711 import HX711



### initializations ###
# Outputs
status_led = Pin(23, Pin.OUT)
servo = PWM(Pin(26), freq(50))

# Inputs
drip_sensor = Pin(14, Pin.IN)   # interrupt for rising and falling edges
pcf_int = Pin(25, Pin.IN)   # interrupt
load_cell = HX711(d_out = 4, pd_sck = 18, channel = 1)  # channel A gain 128

# Protocols
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))



### Constants ###
# Status LED
status_power_on = const()

# Servo motor
servo_home = const()



### power on state ###
def power_on():
    led_status.value(status_power_on)
    # lcd display configure
    servo.duty(servo_home)
    # HMI with LCD updation
    await # wait for start button to be pressed
    

async def run_state_machine():
    state = power_on
    while True:
        state = await state()


loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())
loop.run_forever()
