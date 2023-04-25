### import ###
from machine import Pin, PWM, I2C
from micropython import const
from servo_motor import Servos
from hmi_ui import HMI
import uasyncio, math, gc, time, core_two, _thread, machine
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
load_cell = HX711(d_out = 17, pd_sck = 16, channel = 1)  # channel A gain 128

### Outputs ###
#status_led = Pin(, Pin.OUT)
servo = Servos(i2c_device, addr[2], freq=50)
hmi = HMI(i2c_device, addr[1], addr[0], int_pcf, 101)
nano = Pin(4, Pin.OUT)

### Variables ###
tube_change = 1
drip_rate = 5.0
volume = 0.0

### Flags ###
flag_load_cell = 0
flag_count = 0

### Constants ###
# Status LED
status_power_on = const(1)
status_adjust = const(2)
status_calibrate = const(3)

# Servo motor
servo_home = 0
servo_close = 90

# FSM 
state = None
#hmi_state = hmi.screen_setup


#######################################################################



#######################################################################
#                            '''ISRs'''                               #
#######################################################################
def isr_hmi(pin):
    hmi.int.irq(trigger = 0, handler = None)
    global state
    global flag_load_cell
    global loop
    if flag_load_cell:
        state = idle
    else:
        if hmi.pcf.pin(hmi.button_sel) == 0:
            hmi.sr = "edit"
        elif hmi.pcf.pin(hmi.button_rst) == 0:
            hmi.sr = "reset"
            tube_change = 1
        else:
            hmi.int.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
            return
        y_n = hmi_confirm()
        if y_n:
            return
        hmi.sr = "start"
        state = power_on
    loop.close()
    gc.collect()
    loop = uasyncio.new_event_loop()
    loop.create_task(run_state_machine())
    hmi.int.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
    
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
    return (6000/period) 

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
    core_two.calibrate_load = 1
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
          hmi.state = "setup"
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
async def power_on():
    global state
    global tube_change
    '''hmi.lcd.clear()
    hmi.lcd.putstr("power_on")
    time.sleep(1)'''
    #led_status.value(status_power_on)
    if tube_change:
        servo.position(0, servo_home)
        tube_change = 0
    hmi_setup(hmi.screen_setup, hmi.isr_setup)
    hmi.int.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
    servo.position(0, servo_close)
    #hmi.int.irq(trigger = Pin.IRQ_RISING, handler = set_tsf)
   # await # wait for start button to be pressed
    state = start
    
    
### start state ###
async def start():
    global state
    global drip_rate
    global volume
    '''hmi.lcd.clear()
    hmi.lcd.putstr("start")
    time.sleep(1)'''
    #led_status.value(status_calibrate)
    if abs(drip_rate - hmi.drip_rate) < 19.8:
      state = idle
      return
    else:
      core_two.volume = volume = hmi.volume
      drip_rate = hmi.drip_rate
      state = comp_n_adjust
    
    
### compare and adjust state ###
async def comp_n_adjust():
    global state
    global drip_rate
    '''hmi.lcd.clear()
    hmi.lcd.putstr("comp_n_adjust")
    time.sleep(1)'''
    flag_verify = 0
    while state == comp_n_adjust:
        while True:
            freq = get_freq()
            
            hmi.lcd.clear()
            hmi.lcd.putstr(str(freq))
            hmi.lcd.move_to(0,1)
            hmi.lcd.putstr(str(drip_rate))
            
            if abs(drip_rate - freq) >= 19.8:
                control_servo(drip_rate, freq)
            else:
                if flag_verify:
                    break
                flag_verify = flag_verify + 1
        state = idle
            
    
### Idle state ###
async def idle():
    global state
    '''
    hmi.lcd.clear()
    hmi.lcd.putstr("idle")'''
    hmi.volume = core_two.volume_left
    hmi.time_left = hmi.volume / (5.32 * drip_rate)
    hmi.screen_display()
    while state == idle:
        if hmi.volume - core_two.volume_left > 100:
            hmi.volume = core_two.volume_left
            hmi.time_left = hmi.volume / (5.32 * drip_rate)
            hmi.screen_display()
        
    
#######################################################################


state = power_on
async def run_state_machine():
    global state
    while True:
        await state()

       
### thread safe flag allows interrupts and threads to run along with 
### tasks of the fsm

'''
tsf = uasyncio.ThreadSafeFlag()
def set_tsf(_):
    tsf.set()
    isr_hmi(1)
async def schedule_interrupt():
    while True:
        await tsf.wait()
'''

#hmi.int.irq(trigger = Pin.IRQ_RISING, handler = set_tsf)

_thread.start_new_thread(core_two.critical_core, ())
loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())    # FSM for main tasks
#loop.create_task(schedule_interrupt())   # FSM for interrupts
loop.run_forever()
