from time import sleep
from machine import Pin, PWM, Timer, freq, I2C
import time, math, machine
from servo_motor import Servos
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

machine.freq(240000000)


#####################  Instantiation  #########################
# i2c lcd
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
totalRows = 4
totalColumns = 20
lcd = I2cLcd(i2c, addr[1], totalRows, totalColumns)
# servo
servo = Servos(i2c, addr[2], freq=50)
# ldr
nano = Pin(4, Pin.OUT)
data = Pin(19, Pin.IN)
###############################################################



#########################  Servo  ##############################
def servo_angle(index) -> float:
    return ((servo.degrees/(servo.max_duty - servo.min_duty))*(servo.position(index)-servo.min_duty)) * 90 /103

def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    angle = (servo_angle(0)) - math.ceil((mark - frequency)*slope)
    #else:
    #    angle = (servo_angle(0)) + estimate_turn(mark, freq)
    if angle > 90:
        angle = 90
    elif angle < 20:
        angle = 20
    lcd.move_to(0,3)
    lcd.putstr(str(angle))
    servo.position(0, degrees = ((angle*103)/90))
################################################################


########################### LCD  ###############################
def display_lcd(desired, current):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Desired rate:")
    lcd.move_to(0,1)
    lcd.putstr(str(desired))
    lcd.move_to(0,0)
    lcd.putstr("Drip rate:")
    lcd.move_to(0,1)
    if current < 0.0:
        lcd.putstr("0 drops/sec")
    else:
        lcd.putstr(str(round(current, 1)))
        lcd.putstr(" drops/sec")
################################################################
   
   
   
###################### Frequency count #########################
def get_freq() ->float:
    samples = 10
    count = samples + 1
    no_drop = 0
    stream = 0
    sum_time = 0
    prev_time = 0
    curr_time = 0
    read = 0
    freq_size = 10
    freq = []
    while freq_size:
        flag = 1
        temp = 1
        data_size = 0
        while temp != data.value():
            pass
        while True:
            while True:
                curr_time = time.ticks_us()
                if curr_time - prev_time > 250:
                    read = data.value()
                    break
            prev_time = curr_time
            if read ^ temp:
                flag = flag - 1
                temp = read
            if data_size > 12000:
                if freq_size == 10:
                    lcd.clear()
                    lcd.putstr("Drip Period:")
                lcd.move_to(0,1)
                if read:
                    #t = -1
                    no_drop = no_drop + 1
                    lcd.putstr("No drop   ")
                    #angle = (servo_angle(0) * 90 / 103) - 3
                    #servo.position(0, degrees = angle)
                else:
                    #t = 5000000
                    stream = stream + 1
                    lcd.putstr("Stream   ")
                    #angle = (servo_angle(0) * 90 / 103) + 3
                    #servo.position(0, degrees = angle)
                #freq.append(t) 
                #freq_size = freq_size - 1
                break
            if no_drop == 2:
                return (0.0)
            elif stream == 2:
                return (500.0)
            if flag:
                data_size = data_size + 1 
            else:
                t = data_size * 0.25 #/ 1.85
                if freq_size == 10:
                    lcd.clear()
                    lcd.putstr("Drip Period:")
                lcd.move_to(0,1)
                lcd.putstr(str(t))
                lcd.putstr(" ms   ")
                freq.append(t) 
                freq_size = freq_size - 1
                break
    l = sorted(freq)
    period = l[int(len(l)/ 2)]
    return (1000/period)
################################################################



#########################  start  ##############################
slope = 0
def setup() -> float:
    global slope
    lcd.putstr('calibrate')
    servo.position(0, degrees = 0)
    i = input()
    nano.on()
    servo.position(0, degrees = 83)
    sleep(1)
    nano.off()
    sleep(5)
    freqncy = []
    for i in range(4):
        servo.position(0, degrees = (83 + i))
        freqncy.append(get_freq())
        if i:
            slope = slope + (freqncy[(i-1)]-freqncy[i])
    slope = slope/3
    i = 0
    while get_freq():
        servo.position(0, degrees = (100+i))
    lcd.clear()
    lcd.putstr(str(slope))
    sleep(10)
    return freqncy[3]
################################################################
    


####################### Input ##################################
def rate_input(freqncy) -> float:
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Current drip rate')
    lcd.move_to(0,1)
    lcd.putstr(str(round(freqncy, 2)))
    lcd.move_to(0,2)
    lcd.putstr('Desired drip rate')
    lcd.move_to(0,3)
    mark = float(input('Enter frequency: '))
    return mark
################################################################


freqncy = setup()
flag = 0

while True:
    freqncy
    mark = rate_input(freqncy)
    
    lcd.clear()
    lcd.putstr(str(mark))
    sleep(5)
    lcd.putstr('start')
    
    while True:
        if abs(mark - freqncy) >= 0.25:
            control_servo(mark, freqncy)
        else:
            if flag:
                break
            flag = flag + 1
        freqncy = get_freq()
        display_lcd(mark, freqncy)
        sleep(1)
    lcd.clear()
    lcd.putstr('yaay')
    sleep(3)
