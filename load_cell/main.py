from machine import Pin
from time import sleep
from hx711 import HX711



load_cell = HX711(d_out = 21, pd_sck = 22, channel = 3)

'''
initial = 0
wt = 0

for i in range(100):
    if load_cell.is_ready:
        initial = initial + load_cell.read(raw = False)
initial = initial / 100

print('place weight')
print('initial', initial)
sleep(10)
print('ready')

for i in range(100):
    if load_cell.is_ready:
        wt = wt + initial - load_cell.read(raw = False)
wt = wt / 100
wt = wt / 64.50

print('\ninit reading is    ', initial)
print('\nerror per gram is    ', wt)

'''

while True:
    weight = 0
    for i in range(100):
        if load_cell.is_ready:
            raw_weight = load_cell.read(raw = False)
            weight = weight - 1*((raw_weight+246564.2)/190.5162);
            #weight = weight - (490871 - 244496 + raw_weight)/413
    print(weight/100, 'g')
