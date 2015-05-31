import nxt
import nxt.bluesock
from nxt.motor import *
from nxt.sensor.generic import *
from nxt.sensor.hitechnic import  *
from math import pi

sock = nxt.bluesock.BlueSock('00:16:53:0A:90:46')
brick = sock.connect()

ultra_motor = Motor(brick, PORT_A)
left_motor  = Motor(brick, PORT_B)
right_motor = Motor(brick, PORT_C)

touch_sensor    = Touch(brick, PORT_1)
compass_sensor  = Compass(brick, PORT_2, True)
#color_sensor    = Color20(brick, PORT_3)
ultra_sensor    = Ultrasonic(brick, PORT_4, True)

# Function face_north makes the robot face north.
def face_north():
    global compass_sensor, left_motor, right_motor, revolution
    degree = compass_sensor.get_heading()
    turn_robot(360 - degree)

# Function front_is_clear turns the ultra_motor so that ultra_sensor is
# facing forward. Then it returns True if there's nothing near 50 cm.
# Otherwise it returns False.
def front_is_clear():
    global ultra_motor, ultra_sensor
    face_front()

    if ultra_sensor.get_distance() > 50:
        return True
    else:
        return False

# Function right_is_clear turns the ultra_motor so that ultra_sensor is
# facing right. Then it returns True if there's nothing near 50 cm.
# Otherwise it returns False.
def right_is_clear():
    global ultra_motor, ultra_sensor
    face_right()  
    
    if ultra_sensor.get_distance() > 50:
        return True
    else:
        return False

# Function left_is_clear turns the ultra_motor so that ultra_sensor is
# facing left. Then it returns True if there's nothing near 50 cm.
# Otherwise it returns False.
def left_is_clear():
    global ultra_motor, ultra_sensor
    face_left()

    if ultra_sensor.get_distance() > 50:
        return True
    else:
        return False

# Function face_left makes the ultra_sensor face left.
def face_left():
    global ultra_motor, ultra_sensor
    face_ultra(-90)

# Function face_front makes the ultra_sensor face forward.
def face_front():
    global ultra_motor, ultra_sensor
    face_ultra(0)

# Function face_right makes the ultra_sensor face right.
def face_right():
    global ultra_motor, ultra_sensor
    face_ultra(90)

# Function face_back makes the ultra_sensor face backward.
def face_back():
    global ultra_motor, ultra_sensor
    face_ultra(180)

# Function face_ultra makes the ultra_sensor to x degrees.
# It'll allow error of -5 degree to +5 degree.
# x = 0     : front
# x = -90   : left
# x = 90    : right
# x = 180   : back
def face_ultra(x):
    global ultra_motor, ultra_sensor
    ultra_tacho = ultra_motor.get_tacho()
    
    while True:
        if (x - 5) < ultra_tacho.rotation_count < (x + 5):
            break
        ultra_motor.run(60)
        while True:
            ultra_tacho = ultra_motor.get_tacho()
            if ultra_tacho.rotation_count >= x:
                ultra_motor.brake()
                break
                
        if (x - 5) < ultra_tacho.rotation_count < (x + 5):
            break
        ultra_motor.run(-60)
        while True:
            ultra_tacho = ultra_motor.get_tacho()
            if ultra_tacho.rotation_count <= x:
                ultra_motor.brake()
                break

# Function move_forward makes the robot move straight and stops
# when there's obstacle in front of robot in 50 cm.
# It the robot fail to find the obstacle and touch sensor is pressed,
# robot stops.
def move_forward():
    global ultra_motor, ultra_sensor, touch_sensor
    both_motor = SynchronizedMotors(left_motor, right_motor, 0)
    face_front()
    both_motor.run()
    while True:
        if ultra_sensor.get_distance() < 50:
            both_motor.brake()
            print "distance to wall: ", ultra_sensor.get_distance(), "cm"
            break
        if touch_sensor.is_pressed():
            both_motor.brake()
            print "collision"
            break

# Function move_backward makes the robot move back straight and stops
# when there's obstacle in behind of robot in 100 cm.
def move_backward():
    global ultra_motor, ultra_sensor
    both_motor = SynchronizedMotors(left_motor, right_motor, 0)
    face_back()
    both_motor.run(-100)
    while True:
        if ultra_sensor.get_distance() < 100:
            both_motor.brake()
            print "distance to wall: ", ultra_sensor.get_distance(), "cm"
            break

# Function turn_robot turns the robot x degrees clockwise.
def turn_robot(x):
    global left_motor, right_motor, revolution    
    x = x % 360
    if x <= 180:

        y = x * revolution        
        right_motor.reset_position(False)
        right_tacho = right_motor.get_tacho()
        print right_tacho
        print "right_motor must rotate", y, "degrees"

        while True:
            if abs(right_tacho.rotation_count - y) < 20:
                break
            right_motor.run(70)
            while True:
                right_tacho = right_motor.get_tacho()
                print right_tacho.rotation_count
                if right_tacho.rotation_count >= y:
                    right_motor.brake()
                    break

            if abs(right_tacho.rotation_count - y) < 20:
                break
            right_motor.run(-70)
            while True:
                right_tacho = right_motor.get_tacho()
                print right_tacho.rotation_count
                if right_tacho.rotation_count <= y:
                    right_motor.brake()
                    break
        
    if x > 180:
        x = 360 - x
        y = x * revolution
        left_motor.reset_position(False)
        left_tacho = left_motor.get_tacho()
        print left_tacho
        print "left_motor must rotate", y, "degrees"

        while True:
            if abs(left_tacho.rotation_count - y) < 20:
                break
            left_motor.run(70)
            while True:
                left_tacho = left_motor.get_tacho()
                print left_tacho.rotation_count
                if left_tacho.rotation_count >= y:
                    left_motor.brake()
                    break
                
            if abs(left_tacho.rotation_count - y) < 20:
                break
            left_motor.run(-70)
            while True:
                left_tacho = left_motor.get_tacho()
                print left_tacho.rotation_count
                if left_tacho.rotation_count <= y:
                    left_motor.brake()
                    break

# Function get_revolution computes the revolution of the robot.
def get_revolution():    
    dist = float(raw_input("Distances between two wheels: "))
    radius = float(raw_input("Radius of wheel: "))
    x = 2 * pi * radius
    y = 2 * pi * dist
    revolution = y / x
    return revolution

# Function turn_left makes the robot turn left.
def turn_left():
    global left_motor, right_motor, revolution 
    turn_robot(270)

# Function turn_right makes the robot turn right.
def turn_right():
    global left_motor, right_motor, revolution 
    turn_robot(90)

revolution = get_revolution()
ultra_motor.reset_position(False)
