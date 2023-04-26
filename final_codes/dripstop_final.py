### import ###
from machine import Pin, PWM, I2C, Timer
from servo_motor import Servos
from hmi_ui import HMI
from hx711 import HX711
import math, time, _thread, machine
from hx711 import HX711

machine.freq(240000000)

#######################################################################
#                       ''' Initializations '''                       #
#######################################################################
### Protocols ###
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))
addr = i2c_device.scan()

### Inputs ###
drip_sensor = Pin(19, Pin.IN)   # square pulse from drops
int_pcf = Pin(23, Pin.IN)   # interrupt
load_cell = HX711(d_out = 16, pd_sck = 17, channel = 1)

### Outputs ###
#status_led = Pin(, Pin.OUT)
servo = Servos(i2c_device, addr[2], freq=50)
hmi = HMI(i2c_device, addr[1], addr[0], int_pcf, 101)
nano = Pin(4, Pin.OUT)
buzzer = Pin(18, Pin.OUT)
timer_10_sec = Timer(1)

### Variables ###
tube_change = 1
drip_rate = 5.0
volume = 0.0
# Servo motor
servo_home = 0
servo_close = 102

### Flags ###
flag_load_cell = 0
flag_count = 0


###### CORE TWO ######
core_two_calibrate_load = 0
core_two_volume = 500
core_two_volume_left = 500
core_two_flag = 1

#######################################################################



#######################################################################
#                         '''Core Two'''                              #
#######################################################################
######## Timer Interrupt handler #######
def ISR_Timer(arg):
    timer_10_sec.deinit()      # turn off timer
    servo.position(0, 90)           # 85 degrees

### Interrupt handler for 10% weight ###
def ISR_10_percent():
    global core_two_flag
    timer_10_sec.init(period = 13000, mode = Timer.ONE_SHOT, callback = ISR_Timer)
    buzzer.on()
    t = time.ticks_ms()
    while time.ticks_ms() - t < 700:
        pass
    buzzer.off()
    core_two_flag = 0


def calibrate_load():
    weight = 0
    buzzer.on()
    t = time.ticks_ms()
    while time.ticks_ms() - t < 500:
        pass
    buzzer.off()
    for i in range(100):
        if load_cell.is_ready:
            raw_weight = load_cell.read(raw = False)
            weight = weight + 1*((raw_weight+81752.99)/217.3966)
    return weight / 100


def critical_core():
    global core_two_calibrate_load
    global core_two_volume
    global core_two_volume_left
    global core_two_flag
    weight_ref = 0
    while core_two_flag:
        if core_two_calibrate_load:
            weight_ref = calibrate_load() - volume
            core_two_calibrate_load = 0
        weight = 0
        for i in range(50):
            if load_cell.is_ready:
                raw_weight = load_cell.read(raw = False)
                weight = weight + 1*((raw_weight+81752.99)/217.3966)
        weight = weight / 50
        core_two_volume_left = abs(weight - weight_ref)
        if core_two_volume_left/core_two_volume < 0.1:
            ISR_10_percent()


#######################################################################



#######################################################################
#                            '''ISRs'''                               #
#######################################################################
def isr_hmi(pin):
    hmi.int.irq(trigger = 0, handler = None)
    global flag_load_cell
    global loop
    if flag_load_cell:
        return
    else:
        if hmi.pcf.pin(hmi.button_sel) == 0:
            hmi.sr = "edit"
        elif hmi.pcf.pin(hmi.button_rst) == 0:
            hmi.sr = "reset"
        else:
            hmi.screen_display()
            hmi.int.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
            return
        y_n = hmi_confirm()
        if y_n:
            return
        hmi.sr = "start"
    
#######################################################################



#######################################################################
#                         '''FUNCTIONS'''                             #
#######################################################################
##### Frequency count
def get_freq() ->float:
    no_drop = 0
    stream = 0
    sum_time = 0
    prev_time = 0
    curr_time = 0
    read = 0
    freq_size = 5
    freq = []
    while freq_size:
        flag = 1
        temp = 1
        data_size = 0
        while temp != drip_sensor.value():
            pass
        while True:
            while True:
                curr_time = time.ticks_us()
                if curr_time - prev_time > 250:
                    read = drip_sensor.value()
                    break
            prev_time = curr_time
            if read ^ temp:
                flag = flag - 1
                temp = read
            if data_size > 12000:
                if read:
                    no_drop = no_drop + 1
                else:
                    stream = stream + 1
                break
            if no_drop == 2:
                return (0.0)
            elif stream == 2:
                return (500.0)
            if flag:
                data_size = data_size + 1 
            else:
                t = data_size * 0.25 #/ 1.85
                freq.append(t) 
                freq_size = freq_size - 1
                break
    l = sorted(freq)
    period = l[int(len(l)/ 2)]
    return (60000/period) 

##### Servo control
def servo_angle(index) -> float:
    return ((servo.degrees/(servo.max_duty - servo.min_duty))*(servo.position(index)-servo.min_duty)) * 90 /103

def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    if mark > frequency:
        angle = (servo_angle(0)) + 1
    else:
        angle = (servo_angle(0)) - 1
    if angle < 102:
        angle = 102
    servo.position(0, degrees = ((angle*103)/90))
    
##### Calibrate
def calibrate() -> float:
    global servo_close
    servo.position(0, degrees = servo_close)
    core_two_volume = volume = hmi.volume
    core_two_calibrate_load = 1
    hmi.animate_drops(4, 14, 3)
    nano.on()
    servo.position(0, degrees = 78)
    # no needle 77
    # medium needle 82
    time.sleep(1)
    nano.off()
    hmi.animate_drops(4, 14, 3)
    i = 0
    while get_freq():
        servo.position(0, degrees = (90+i))
        i = i + 1
    servo_close = 90 + i
    return 0.0
  
##### HMI 
def hmi_confirm():
    hmi.screen_confirm()
    y_n = 0
    while hmi.pcf.pin(hmi.button_sel):
        if hmi.pcf.pin(hmi.button_inc) == 0:
            y_n = 1
        elif hmi.pcf.pin(hmi.button_dec) == 0:
            y_n = 0
    return y_n
  
def hmi_setup(state, isr):
  global drip_rate
  while True:
      state()
      hmi.int.irq(trigger = Pin.IRQ_FALLING, handler = isr)
      if hmi.state == "calibrate":
          drip_rate = calibrate()
          hmi.flag_irq = 1
      while True:
          if hmi.flag_irq:
              hmi.int.irq(handler = None, trigger = 0)
              hmi.flag_irq = 0
              break
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
      elif hmi.state == "done":
          hmi.screen_display()
          state = hmi.screen_setup
          isr = hmi.isr_setup
          break 
#######################################################################



#######################################################################
#                           '''STATES'''                              #
#######################################################################
### power on state ###
def power_on():
    global tube_change
    global core_two_calibrate_load
    '''hmi.lcd.clear()
    hmi.lcd.putstr("power_on")
    time.sleep(1)'''
    if tube_change:
        servo.position(0, servo_home)
        tube_change = 0
    hmi_setup(hmi.screen_setup, hmi.isr_setup)
    hmi.int.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
    core_two_calibrate_load = 1
    servo.position(0, servo_close)
    

### start state ###
def start():
    global drip_rate
    global volume
    '''hmi.lcd.clear()
    hmi.lcd.putstr("start")
    time.sleep(1)'''
    if abs(drip_rate - hmi.drip_rate)/drip_rate < 0.3:
      return
    else:
      core_two_volume = volume = hmi.volume
      drip_rate = hmi.drip_rate
      

### compare and adjust state ###
def comp_n_adjust():
    global drip_rate
    '''hmi.lcd.clear()
    hmi.lcd.putstr("comp_n_adjust")
    time.sleep(1)'''
    flag_verify = 0
    while True:
        freq = get_freq()
        hmi.lcd.clear()
        hmi.lcd.putstr(str(freq))
        hmi.lcd.move_to(0,1)
        hmi.lcd.putstr(str(drip_rate))
        if abs(drip_rate - freq)/drip_rate >= 0.3:
            control_servo(drip_rate, freq)
        else:
            if flag_verify:
                break
            flag_verify = flag_verify + 1
            

### Idle state ###
def idle():
    global core_two_volume_left
    global drip_rate
    hmi.volume = core_two_volume_left
    hmi.time_left = (hmi.volume * 5.32) /  drip_rate
    hmi.screen_display()
    while True:
        if hmi.volume - core_two_volume_left > 5:
            hmi.consumed = (core_two_volume - core_two_volume_left) * 100 / core_two_volume
            hmi.volume = core_two_volume_left
            hmi.time_left = (hmi.volume * 5.32) / drip_rate
            hmi.screen_display()

#######################################################################


_thread.start_new_thread(critical_core, ())
power_on()
start()
comp_n_adjust()
idle()
