### import ###
from machine import Pin, PWM, I2C
from micropython import const
from time
from servo_motor import Servos
from hmi_ui import HMI
import uasyncio, math, gc
from hx711 import HX711



#######################################################################
                         ''' Initializations '''
#######################################################################
### Protocols ###
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))
addr = i2c_device.scan()

### Outputs ###
#status_led = Pin(, Pin.OUT)
servo = Servos(i2c, addr[2], freq=50)
hmi = HMI(i2c, addr[1], addr[0], int_pcf, 101)
nano = Pin(4, Pin.OUT)

### Inputs ###
drip_sensor = Pin(19, Pin.IN)   # square pulse from drops
int_pcf = Pin(23, Pin.IN)   # interrupt
load_cell = HX711(d_out = 17, pd_sck = 16, channel = 1)  # channel A gain 128

### Variables ###
tube_change = 1
drip_rate = 0.0
volume = 0.0

### Flags ###
flag_load_cell = 0
flag_count = 0

### Constants ###
# Status LED
status_power_on = const()
status_adjust = const()
status_calibrate = const()

# Servo motor
servo_home = 0
servo_close = 90
servo_step = 0

# FSM 
state = None
#hmi_state = hmi.screen_setup


#######################################################################



#######################################################################
                             '''ISRs'''
#######################################################################
def isr_hmi(pin):
  global flag_load_cell
  if flag_load_cell:
    state = idle
  else:
    int_pcf.irq(trigger = 0, handle = None)
    if hmi.button_strt == 0:
      hmi.sr = "edit"
    elif hmi.button_rst == 0:
      hmi.sr = "reset"
      tube_change = 1
    hmi_confirm()
    hmi.sr = "start"
    state = power_on
  # (volume xor hmi.volume) or (drip_rate xor hmi.drip_rate):   # data from pcf 
  loop.close()
  gc.collect()
  loop = uasyncio.new_event_loop()
  loop.create_task(run_state_machine())
    
#######################################################################



#######################################################################
                          '''FUNCTIONS'''
#######################################################################
##### Frequency count
def get_freq() ->float:
    samples = 5
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
                if freq_size == 10:
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
                t = data_size * 0.25 # sample size * data count
                freq.append(t) 
                freq_size = freq_size - 1
                break
    l = sorted(freq)
    period = l[int(len(l)/ 2)]
    return (1000/period)

##### Servo control
def servo_angle(index) -> float:
    return ((servo.degrees/(servo.max_duty - servo.min_duty))*(servo.position(index)-servo.min_duty)) * 90 /103

def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    if mark > frequency:
        angle = (servo_angle(0)) + 1
    else:
        angle = (servo_angle(0)) - 1
    if angle < 97:
        angle = 98
    servo.position(0, degrees = ((angle*103)/90))
    
##### Calibrate
def calibrate(): -> float:
    global servo_close
    servo.position(0, degrees = 0)
    i = input()
    nano.on()
    servo.position(0, degrees = 78)
    # no needle 77
    # medium needle 82
    sleep(1)
    nano.off()
    hmi.animate_drops
    i = 0
    while get_freq():
        servo.position(0, degrees = (90+i))
        i = i + 1
    servo_close = 90 + i
    return 0.0
  
##### HMI 
def hmi_confirm():
  hmi.screen_confirm()
  hmi.int.irq(trigger = Pin.IRQ_FALLING, handler = hmi.isr_confirm)
  while True:
          if hmi.flag_irq:
              hmi.int.irq(handler = None, trigger = 0)
              hmi.flag_irq = 0
              break
  
def hmi_setup(state, isr):
  global drip_rate
  #state = hmi.screen_setup
  #isr = hmi.isr_setup
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
          isr = hmi.isr_continue
      elif hmi.state == "done":
          hmi.screen_display()
          state = hmi.screen_setup
          isr = hmi.isr_setup
          break 
#######################################################################



#######################################################################
                            '''STATES'''
#######################################################################
### power on state ###
async def power_on():
    global state
    #led_status.value(status_power_on)
    if tube_change:
        servo.position(servo_home)
        tube_change = 0
    setup_hmi(hmi.screen_setup, hmi.isr_setup)
    int_pcf.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)
   # await # wait for start button to be pressed
    state = start 
    
    
### start state ###
async def start():
    global state
    #led_status.value(status_calibrate)
    if (drip_rate - hmi.drip_rate < 0.48) and (volume - 
    # check for current rate and calculated 
    # switch to idle or adjust acc
    state = comp_n_adjust
    
    
### compare and adjust state ###
async def comp_n_adjust():
    global state
    flag_verify = 0
    while state == comp_n_adjust:
        while True:
          freq = get_freq()
          if abs(drip_rate - freq) >= 0.25:
              control_servo(drip_rate, freq)
          else:
              if flag_verify:
                  break
              flag_verify = flag_verify + 1
        return idle
            
    
### Idle state ###
async def idle():
    global state
    while state == idle:
        pass
    
#######################################################################


state = power_on
async def run_state_machine():
    global state
    while True:
        state = await state()

       
### thread safe flag allows interrupts and threads to run along with 
### tasks of the fsm
'''
tsf = uasyncio.ThreadSafeFlag()

def set_tsf(_):
    tsf.set()
    HMI_ISR()

async def schedule_interrupt():
    while True:
        await tsf.wait()
'''

int_pcf.irq(trigger = Pin.IRQ_RISING, handler = isr_hmi)

loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())    # FSM for main tasks
#loop.create_task(schedule_interrupt())   # FSM for interrupts
loop.run_forever()
