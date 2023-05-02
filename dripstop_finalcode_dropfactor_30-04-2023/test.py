import core_two, _thread, time


_thread.start_new_thread(core_two.critical_core, ())
core_two.calibrate_load = 1
t = 0

while time.ticks_ms() - t < 10000:
        pass


for i in range(7):
    print(core_two.volume_left)
    t = time.ticks_ms()
    while time.ticks_ms() - t < 10000:
        pass

_thread.exit()