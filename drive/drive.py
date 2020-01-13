import time


def run(dxl_io, motors):
    for motor in motors:
        motor.set_velocity_mode()
        motor.torque_enable()

    while True:
        time.sleep(2)
        for motor in motors:
            motor.set_velocity(30)
        time.sleep(2)
        for motor in motors:
            motor.set_velocity(0)
        time.sleep(2)
        for motor in motors[0:2]:
            motor.set_velocity(30)
        for motor in motors[2:]:
            motor.set_velocity(-30)
        time.sleep(2)
        for motor in motors:
            motor.set_velocity(0)
