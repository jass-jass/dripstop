### import ###
from machine import Pin, PWM, I2C
from micropython import const
from time
from servo_motor import Servos
from hmi_ui import HMI_UI
import uasyncio, math
from hx711 import HX711



#######################################################################
                         ''' Initializations '''
#######################################################################
### Protocols ###
i2c_device = I2C(0, scl = Pin(22), sda = Pin(21))
addr = i2c_device.scan()

### Outputs ###
status_led = Pin(23, Pin.OUT)
servo = Servos(i2c, addr[0], freq=50)
hmi = HMI_UI(addr[1], addr[0], int_pcf, 101)
nano = Pin(4, Pin.OUT)

### Inputs ###
drip_sensor = Pin(19, Pin.IN)   # square pulse from drops
int_pcf= Pin(23, Pin.IN)   # interrupt
load_cell = HX711(d_out = 4, pd_sck = 18, channel = 1)  # channel A gain 128

### Variables ###
tube_change = 1
drip_rate = 0
slope = 0

### Flags ###
load_cell_flag = 0
count_flag = 0

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
state = power_on


#######################################################################



#######################################################################
                             '''ISRs'''
#######################################################################
def HMI_ISR():
  global load_cell_flag
  global input_array
  if load_cell_flag:
    # disable interrupt
    # return to idle
  elif input_array xor :   # data from pcf


#######################################################################



#######################################################################
                          '''FUNCTIONS'''
#######################################################################
##### Frequency count
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
                    lcd.clear()
                    lcd.putstr("Drip Period:")
                lcd.move_to(0,1)
                if read:
                    #t = -1
                    no_drop = no_drop + 1
                    lcd.putstr("No drop   ")
                else:
                    stream = stream + 1
                    lcd.putstr("Stream   ")
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

##### Servo control
def servo_angle(index) -> float:
    return ((servo.degrees/(servo.max_duty - servo.min_duty))*(servo.position(index)-servo.min_duty)) * 90 /103

def control_servo(mark, frequency):
    # greater the frequency, lesser the angle
    angle = (servo_angle(0)) - math.ceil((mark - frequency)*slope)
    if angle > 90:
        angle = 90
    elif angle < 20:
        angle = 20
    lcd.move_to(0,3)
    lcd.putstr(str(angle))
    servo.position(0, degrees = ((angle*103)/90))
    
##### Calibrate
def calibrate() -> float:
    global slope
    global servo_home
    servo.position(0, degrees = 0)
    nano.on()
    servo.position(0, degrees = 83)
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
    servo_close = servo_angle(0)
    return freqncy[3]
#######################################################################



#######################################################################
                            '''STATES'''
#######################################################################
### power on state ###
async def power_on():
    global state
    led_status.value(status_power_on)
    # lcd display configure
    if tube_change:
        servo.position(servo_home)
        tube_change = 0
    # HMI with LCD updation
    await # wait for start button to be pressed
    
    
### start state ###
async def start():
    global state
    servo.duty(servo_close)
    led_status.value(status_calibrate)
    drip_rate = # calculate drip rate
    # check for current rate and calculated 
    # switch to idle or adjust acc
    
    
### compare and adjust state ###
async def comp_n_adjust():
    global state
    flag_verify = 0
    while state == comp_n_adjust:
        while True:
          freq = get_freq()
          if abs(drip_rate - freq) >= 0.1:
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



async def run_state_machine():
    global state
    while True:
        state = await state()

       
### thread safe flag allows interrupts and threads to run along with 
### tasks of the fsm
tsf = uasyncio.ThreadSafeFlag()

def set_tsf(_):
    tsf.set()
    HMI_ISR()

async def schedule_interrupt():
    while True:
        await tsf.wait()

int_pcf.irq(trigger = Pin.IRQ_RISING, handler = set_tsf)

loop = uasyncio.get_event_loop()
loop.create_task(run_state_machine())    # FSM for main tasks
loop.create_task(schedule_interrupt())   # FSM for interrupts
loop.run_forever()
