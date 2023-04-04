from machine import Pin, PWM, Timer, freq, I2C
import sh1106
import time, math
import machine as mac

mac.freq(240000000)


### PWM generation
timer = Timer(1)
pwm_out = Pin(23, Pin.OUT)

def pwm_off(timer):
    timer.init(period=20, mode=Timer.ONE_SHOT, callback=pwm_on)
    pwm_out.off()

def pwm_on(timer):
    timer.init(period=50, mode=Timer.ONE_SHOT, callback=pwm_off)
    pwm_out.on()

timer.init(period=20, mode=Timer.ONE_SHOT, callback=pwm_on)



### OLED display  
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
print(addr)


i2c = I2C(0)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), addr[0], rotate=0, delay=0)


def oled_disp(text, numeral):
    display.sleep(False)
    display.fill(0)
    display.text(text, 0, 0, 1)
    display.text(str(numeral), 0, 8, 1)
    display.show()



### Frequency count
samples = 10
count = samples + 1
prev_time = 0
curr_time = 0
sum_time = 0

oled_disp('address', addr[0])


def timer_period(data):
    global prev_time
    global curr_time
    global count
    global sum_time
    curr_time = time.ticks_us()
    if count < samples:
        sum_time = sum_time + curr_time - prev_time
    count = count - 1
    prev_time = curr_time
    if count == 0:
        data.irq(trigger = 0, handler = None)


data = Pin(34, Pin.IN)
data.irq(handler = timer_period, trigger = Pin.IRQ_FALLING)


while True:
    arr_freq = []
    arr_size = 10
    while arr_size:
        if count == 0:
            t_period = ( sum_time / samples ) /1000 / 0.9
            if t_period:
                arr_freq.append(1000/t_period)
            else:
                pass
            oled_disp('period', t_period)
            arr_size = arr_size - 1
            sum_time = 0
            count = samples
            if arr_size:
                data.irq(handler = timer_period, trigger = Pin.IRQ_FALLING)
    ##############################################################
    l = sorted(arr_freq)
    freq = l[int(len(l)/ 2)]
    oled_disp('freq', freq)
    data.irq(handler = timer_period, trigger = Pin.IRQ_FALLING)
