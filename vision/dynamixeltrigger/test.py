from dynamixeltrigger import DynaTrigger as dyn
from dynio import *
import threading

dxl_io = dxl.DynamixelIO("/dev/ttyUSB0")

print("Running")
trigger1 = dyn(dxl_io.new_ax12(9), 1023, None)
trigger2 = dyn(dxl_io.new_ax12(10), 637, None)
trigger3 = dyn(dxl_io.new_ax12(11), 9, None)
trigger4 = dyn(dxl_io.new_ax12(12), 9, None)
print("Still Running")

thread1 = threading.Thread(target=trigger1.Run(),args=())
thread1.daemon = True
thread2 = threading.Thread(target=trigger2.Run(),args=())
thread2.daemon = True
thread3 = threading.Thread(target=trigger3.Run(),args=())
thread3.daemon = True
thread4 = threading.Thread(target=trigger4.Run(),args=())
thread4.daemon = True

thread2.start()
thread1.start()
thread3.start()
thread4.start()

# motor = dxl_io.new_ax12(12)
# motor.torque_disable()
#
# while True:
#     print(motor.get_position())
