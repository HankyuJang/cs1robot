import nxt
import nxt.bluesock
from nxt.motor import *
from nxt.sensor.generic import *
from nxt.sensor.hitechnic import  *
from math import pi

class Robot(object):
    def __init__(self, ultra_left_right_motor, touch_compass_sound_ultra_sensor):
        self.ultra_motor, self.left_motor, self.right_motor = ultra_left_right_motor        
        self.touch_sensor, self.compass_sensor, self.sound_sensor, self.ultra_sensor = \
        touch_compass_sound_ultra_sensor

        self.revolution = self.get_revolution()
        self.ultra_motor.reset_position(False)

    # Function is_clapped returns True when clapped.
    def is_clapped(self):
        return self.sound_sensor.get_loudness() > 500

    # Function face_north makes the robot face north.
    def face_north(self):
        degree = self.compass_sensor.get_heading()
        self.turn_robot(360 - degree)

    # Function front_is_clear turns the self.ultra_motor so that self.ultra_sensor is
    # facing forward. Then it returns True if there's nothing near 50 cm.
    # Otherwise it returns False.
    def front_is_clear(self):
        self.face_front()

        if self.ultra_sensor.get_distance() > 50:
            return True
        else:
            return False

    # Function right_is_clear turns the self.ultra_motor so that self.ultra_sensor is
    # facing right. Then it returns True if there's nothing near 50 cm.
    # Otherwise it returns False.
    def right_is_clear(self):
        self.face_right()  
        
        if self.ultra_sensor.get_distance() > 50:
            return True
        else:
            return False

    # Function left_is_clear turns the self.ultra_motor so that self.ultra_sensor is
    # facing left. Then it returns True if there's nothing near 50 cm.
    # Otherwise it returns False.
    def left_is_clear(self):
        self.face_left()

        if self.ultra_sensor.get_distance() > 50:
            return True
        else:
            return False

    # Function face_left makes the self.ultra_sensor face left.
    def face_left(self):
        self.face_ultra(-90)

    # Function face_front makes the self.ultra_sensor face forward.
    def face_front(self):
        self.face_ultra(0)

    # Function face_right makes the self.ultra_sensor face right.
    def face_right(self):
        self.face_ultra(90)

    # Function face_back makes the self.ultra_sensor face backward.
    def face_back(self):
        self.face_ultra(180)

    # Function face_ultra makes the self.ultra_sensor to x degrees.
    # It'll allow error of -5 degree to +5 degree.
    # x = 0     : front
    # x = -90   : left
    # x = 90    : right
    # x = 180   : back
    def face_ultra(self, x):
        ultra_tacho = self.ultra_motor.get_tacho()
        
        while True:
            if (x - 5) < ultra_tacho.rotation_count < (x + 5):
                break
            self.ultra_motor.run(60)
            while True:
                ultra_tacho = self.ultra_motor.get_tacho()
                if ultra_tacho.rotation_count >= x:
                    self.ultra_motor.brake()
                    break
                    
            if (x - 5) < ultra_tacho.rotation_count < (x + 5):
                break
            self.ultra_motor.run(-60)
            while True:
                ultra_tacho = self.ultra_motor.get_tacho()
                if ultra_tacho.rotation_count <= x:
                    self.ultra_motor.brake()
                    break

    # Function move_forward makes the robot move straight and stops
    # when there's obstacle in front of robot in 50 cm.
    # It the robot fail to find the obstacle and touch sensor is pressed,
    # robot stops.
    def move_forward(self):
        both_motor = SynchronizedMotors(self.left_motor, self.right_motor, 0)
        self.face_front()
        both_motor.run()
        while True:
            if self.ultra_sensor.get_distance() < 50:
                both_motor.brake()
                print "distance to wall: ", self.ultra_sensor.get_distance(), "cm"
                break
            if self.touch_sensor.is_pressed():
                both_motor.brake()
                print "collision"

                both_motor.turn(-100, 500)          
                
                break

    # Function move_backward makes the robot move back straight and stops
    # when there's obstacle in behind of robot in 100 cm.
    def move_backward(self):
        both_motor = SynchronizedMotors(self.left_motor, self.right_motor, 0)
        self.face_back()
        both_motor.run(-100)
        while True:
            if self.ultra_sensor.get_distance() < 100:
                both_motor.brake()
                print "distance to wall: ", self.ultra_sensor.get_distance(), "cm"
                break

    # Function turn_robot turns the robot x degrees clockwise.
    def turn_robot(self, x):  
        x = x % 360
        if x <= 180:

            y = x * self.revolution        
            self.right_motor.reset_position(False)
            right_tacho = self.right_motor.get_tacho()
            print right_tacho
            print "right_motor must rotate", y, "degrees"

            while True:
                if abs(right_tacho.rotation_count - y) < 20:
                    break
                self.right_motor.run(70)
                while True:
                    right_tacho = self.right_motor.get_tacho()
                    print right_tacho.rotation_count
                    if right_tacho.rotation_count >= y:
                        self.right_motor.brake()
                        break

                if abs(right_tacho.rotation_count - y) < 20:
                    break
                self.right_motor.run(-70)
                while True:
                    right_tacho = self.right_motor.get_tacho()
                    print right_tacho.rotation_count
                    if right_tacho.rotation_count <= y:
                        self.right_motor.brake()
                        break
            
        if x > 180:
            x = 360 - x
            y = x * self.revolution
            self.left_motor.reset_position(False)
            left_tacho = self.left_motor.get_tacho()
            print left_tacho
            print "left_motor must rotate", y, "degrees"

            while True:
                if abs(left_tacho.rotation_count - y) < 20:
                    break
                self.left_motor.run(70)
                while True:
                    left_tacho = self.left_motor.get_tacho()
                    print left_tacho.rotation_count
                    if left_tacho.rotation_count >= y:
                        self.left_motor.brake()
                        break
                    
                if abs(left_tacho.rotation_count - y) < 20:
                    break
                self.left_motor.run(-70)
                while True:
                    left_tacho = self.left_motor.get_tacho()
                    print left_tacho.rotation_count
                    if left_tacho.rotation_count <= y:
                        self.left_motor.brake()
                        break

    # Function get_revolution computes the self.revolution of the robot.
    def get_revolution(self):    
        dist = float(raw_input("Distances between two wheels: "))
        radius = float(raw_input("Radius of wheel: "))
        x = 2 * pi * radius
        y = 2 * pi * dist
        revolution = y / x
        return revolution

    # Function turn_left makes the robot turn left.
    def turn_left(self):
        self.turn_robot(270)

    # Function turn_right makes the robot turn right.
    def turn_right(self):
        self.turn_robot(90)

