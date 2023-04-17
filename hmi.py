from machine import Pin, I2C
import time
from hmi_ui import HMI



i2c = I2C(0, scl = Pin(22), sda = Pin(21), freq = 1000)
addr = i2c.scan()
int_pcf = Pin(23, Pin.IN)
ID = 100
hmi = HMI(i2c, addr[1], addr[0], int_pcf, ID)

state = hmi.screen_setup
isr = hmi.isr_setup
while True:
    state()
    hmi.int.irq(trigger = Pin.IRQ_FALLING, handler = isr)
    if hmi.state == "calibrate":
        hmi.animate_drops(4, 14, 3)
        hmi.flag_irq = 1
    while True:
        if hmi.flag_irq:
            hmi.int.irq(handler = None, trigger = 0)
            hmi.flag_irq = 0
            break
    print(hmi.state)
    if hmi.state == "setup":
        state = hmi.screen_setup
        isr = hmi.isr_setup
    elif hmi.state == "confirm":
        hmi.screen_display()
        time.sleep(1)
        state = hmi.screen_confirm
        isr = hmi.isr_confirm
    elif hmi.state == "calibrate":
        state = hmi.screen_calibrate
        isr = hmi.isr_continue
        #hmi.state = "confirm"
        #state = hmi.screen_display
        #isr = hmi.isr_continue
    elif hmi.state == "done":
        hmi.screen_display()
        state = hmi.screen_setup
        isr = hmi.isr_setup
        break
