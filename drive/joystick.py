from evdev import list_devices, InputDevice, categorize, ecodes
import math


def joystick_to_diff(x, y, min_joystick, max_joystick, min_speed,
                     max_speed):  # If x and y are 0, then there is not much to calculate...
    if x == 0 and y == 0:
        return 0, 0

    # First Compute the angle in deg
    # First hypotenuse
    z = math.sqrt(x * x + y * y)

    # angle in radians
    rad = math.acos(math.fabs(x) / z)

    # and in degrees
    angle = rad * 180 / math.pi

    # Now angle indicates the measure of turn
    # Along a straight line, with an angle o, the turn co-efficient is same
    # this applies for angles between 0-90, with angle 0 the coeff is -1
    # with angle 45, the co-efficient is 0 and with angle 90, it is 1

    tcoeff = -1 + (angle / 90) * 2
    turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
    turn = round(turn * 100, 0) / 100

    # And max of y or x is the movement
    mov = max(math.fabs(y), math.fabs(x))

    # First and third quadrant
    if (x >= 0 and y >= 0) or (x < 0 and y < 0):
        raw_left = mov
        raw_right = turn
    else:
        raw_right = mov
        raw_left = turn

    # Reverse polarity
    if y < 0:
        raw_left = 0 - raw_left
        raw_right = 0 - raw_right

    # minJoystick, maxJoystick, minSpeed, maxSpeed
    # Map the values onto the defined rang
    right_out = remap(raw_right, min_joystick, max_joystick, min_speed, max_speed)
    left_out = remap(raw_left, min_joystick, max_joystick, min_speed, max_speed)

    return right_out, left_out


def remap(v, in_min, in_max, out_min, out_max):
    # Check that the value is at least in_min
    if v < in_min:
        v = in_min
    # Check that the value is at most in_max
    if v > in_max:
        v = in_max
    return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def run(dxl_io, motors):
    for motor in motors:
        motor.set_velocity_mode()
        motor.torque_enable()

    CENTER_TOLERANCE = 350
    STICK_MAX = 65536

    dev = InputDevice("/dev/input/event2")
    axis = {
        ecodes.ABS_X: 'ls_x',  # 0 - 65,536   the middle is 32768
        ecodes.ABS_Y: 'ls_y',
        ecodes.ABS_Z: 'rs_x',
        ecodes.ABS_RZ: 'rs_y',
        ecodes.ABS_BRAKE: 'lt',  # 0 - 1023
        ecodes.ABS_GAS: 'rt',

        ecodes.ABS_HAT0X: 'dpad_x',  # -1 - 1
        ecodes.ABS_HAT0Y: 'dpad_y'
    }

    center = {
        'ls_x': STICK_MAX / 2,
        'ls_y': STICK_MAX / 2,
        'rs_x': STICK_MAX / 2,
        'rs_y': STICK_MAX / 2
    }

    last = {
        'ls_x': STICK_MAX / 2,
        'ls_y': STICK_MAX / 2,
        'rs_x': STICK_MAX / 2,
        'rs_y': STICK_MAX / 2
    }

    for event in dev.read_loop():

        # calibrate zero on Y button
        if event.type == ecodes.EV_KEY:
            if categorize(event).keycode[0] == "BTN_WEST":
                center['ls_x'] = last['ls_x']
                center['ls_y'] = last['ls_y']
                center['rs_x'] = last['rs_x']
                center['rs_y'] = last['rs_y']
                print('calibrated')

        # read stick axis movement
        elif event.type == ecodes.EV_ABS:
            if event.code in axis and axis[event.code] in ['ls_x', 'ls_y']:
                last[axis[event.code]] = event.value

                value = event.value - center[axis[event.code]]

                if abs(value) <= CENTER_TOLERANCE:
                    value = 0

                if axis[event.code] == 'ls_x':
                    if value < 0:
                        print('left')
                    else:
                        print('right')
                    print(value)

                elif axis[event.code] == 'ls_y':
                    if value < 0:
                        print('forward')
                    else:
                        print('backward')
                    print(value)

                # Send robot command
                right, left = joystick_to_diff(last["ls_y"], last["ls_x"], -32768, 32768, -300, 300)

                for motor in motors[0:2]:
                    motor.set_velocity(int(right))

                for motor in motors[2:]:
                    motor.set_velocity(int(left))
