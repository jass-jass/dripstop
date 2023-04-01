from machine import Pin, PWM, Timer, freq, I2C
import sh1106
import time, math
import machine as mac

mac.freq(240000000)


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), addr[0], rotate=0, delay=0)


def oled_disp(cyc, on, off, freq):
    strng = str(on)+ ' '+ str(off)+ ' '+ str(freq)
    display.sleep(False)
    display.fill(0)
    display.text(str(cyc), 0, 0, 1)
    display.text('on '+ str(on), 0, 8, 1)
    display.text('off '+ str(off), 0, 16, 1)
    display.text('freq '+ str(freq), 0, 24, 1)
    display.show()



### Frequency count
samples = 10
on_count = samples 
off_count = samples 
on_time = 0
off_time = 0
on_sum = 0
off_sum = 0


def timer_on(data):
    global on_time
    global on_sum
    global on_count
    on_time = time.ticks_us()
    if on_count < samples:
        on_sum = on_sum + on_time - off_time
    if on_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
    on_count = on_count - 1

def timer_off(data):
    global off_time
    global off_sum
    global off_count
    off_time = time.ticks_us()
    if off_count < samples:
        off_sum = off_sum + off_time - on_time
    if off_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)
    off_count = off_count - 1


data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


cycle = 1
while True:
    if on_count == 0 or off_count == 0:
        on = (on_sum / samples )
        off = (off_sum / samples ) 
        t_period = (on + off)/1000000
        if t_period:
            freq = 1/t_period
        oled_disp(cycle, on, off, freq)
        cycle = cycle + 1
        on_sum = 0
        off_sum = 0
        on_count = off_count = samples
        data.irq(handler = timer_on, trigger = Pin.IRQ_RISING)
