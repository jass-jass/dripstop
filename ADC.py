from machine import Pin, ADC, PWM
from time import sleep

led = PWM(Pin(18), freq=50)
pot = ADC(Pin(4))
pot.atten(ADC.ATTN_11DB)
# ADC.ATTN_0DB    full range 1.2V
# ADC.ATTN_2_5DB  full range 1.5V
# ADC.ATTN_6DB    full range 2.0V
# ADC.ATTN_11DB   full range 3.3V

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return int(scaled_value)

while True:
  pot_value = pot.read()
  print(pot_value)
  led.duty(scale_value(pot_value, 0, 4095, 0, 1023))
  #sleep(1)
