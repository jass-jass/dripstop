from machine import Pin, PWM, Timer, freq, I2C
import sh1106
import time, math
import machine as mac

mac.freq(240000000)



timer = Timer(1)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=7, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=3, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=1, mode=Timer.ONE_SHOT, callback=pwm_on)


    
    
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), addr[0], rotate=0, delay=0)


def oled_disp(text, numeral):
    display.sleep(False)
    display.fill(0)
    display.text(text+' '+str(numeral), 0, 0, 1)
    display.show()



### Frequency count
samples = 10
on_count = samples + 1
off_count = samples + 1
on_time = 0
off_time = 0
on_sum = 0
off_sum = 0


def timer_on(data):
    global on_time
    global on_sum
    global on_count
    on_time = time.ticks_us()
    if on_count <= samples:
        on_sum = on_sum + on_time - off_time
    on_count = on_count - 1
    if on_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)

def timer_off(data):
    global off_time
    global off_sum
    global off_count
    off_time = time.ticks_us()
    if off_count <= samples:
        off_sum = off_sum + off_time - on_time
    off_count = off_count - 1
    if off_count == 0:
        data.irq(trigger = 0, handler = None)
    else:
        data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


data = Pin(34, Pin.IN)
data.irq(handler = timer_on, trigger = Pin.IRQ_FALLING)


while True:
    arr_freq = []
    arr_size = 10
    while arr_size:
        if on_count == 0 or off_count == 0:
            on = (on_sum / samples ) + 200
            off = (off_sum / samples )
            t_period = (on + off)/1000000
            if t_period:
                arr_freq.append(1/t_period)
            else:
                pass
#             oled_disp(str(10 - arr_size), arr_freq[10-arr_size])
            oled_disp(str(on), off)
            arr_size = arr_size - 1
            on_sum = 0
            off_sum = 0
            on_count = off_count = samples
            if arr_size:
                data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)
    ##############################################################
    l = sorted(arr_freq)
    freq = l[int(len(l)/ 2)]
    oled_disp('freq', freq)
    time.sleep(2)
    data.irq(handler = timer_off, trigger = Pin.IRQ_RISING)