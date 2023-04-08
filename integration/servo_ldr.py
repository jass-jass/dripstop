from time import sleep
from machine import Pin, PWM, Timer, freq, I2C
import servo, time, math, machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

machine.freq(240000000)


#####################  Instantiation  #########################
# servo
servo = servo.Servo(4)
# i2c lcd
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = i2c.scan()
totalRows = 4
totalColumns = 20
lcd = I2cLcd(i2c, addr[0], totalRows, totalColumns)
# ldr
data = Pin(34, Pin.IN)
###############################################################



#########################  Servo  ##############################
def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    if mark > frequency:
        angle = servo.read() - 2
    else:
        angle = servo.read() + 2 
    servo.write(angle)
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
    sum_time = 0
    prev_time = 0
    curr_time = 0
    read = 0
    freq_size = 10
    freq = []
    while freq_size:
        flag = 2
        temp = 0
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
                    t = -1
                    lcd.putstr("No drop   ")
                else:
                    t = 5000000
                    lcd.putstr("Stream   ")
                freq.append(t) 
                freq_size = freq_size - 1
                break
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
servo.write(0)
#lcd.putstr('Place tube')
#p = input('start [y/n]')
servo.write(90)
################################################################
    
freq = 0
cheat = 1
    
while True:
    # 0.6 to 25 Hz
    '''
    mark = 25
    while mark >= 1:
        flag = 0
        while True:
            freq = get_freq()
            display_lcd(freq)
            if mark ^ int(freq):
                control_servo(mark, freq)
            else:
                if flag:
                    break
                flag = flag + 1
    '''
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Current drip rate')
    lcd.move_to(0,1)
    lcd.putstr(str(round(freq, 2)))
    lcd.move_to(0,2)
    lcd.putstr('Desired drip rate')
    lcd.move_to(0,3)
    flag = 0
    mark = 1.6
    lcd.putstr(str(mark))
    sleep(10)
    if cheat:
        servo.write(84)
        cheat = cheat - 1
    while True:
        freq = get_freq()
        display_lcd(mark, freq)
        if abs(mark - freq) >= 0.1:
            control_servo(mark, freq)
        else:
            if flag:
                break
            flag = flag + 1
