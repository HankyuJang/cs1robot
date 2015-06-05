from cs1robot import *

sock = nxt.bluesock.BlueSock('00:16:53:0A:90:46')
brick = sock.connect()

ultra_motor = Motor(brick, PORT_A)
left_motor  = Motor(brick, PORT_B)
right_motor = Motor(brick, PORT_C)

touch_sensor    = Touch(brick, PORT_1)
compass_sensor  = Compass(brick, PORT_2)
sound_sensor    = Sound(brick, PORT_3)
ultra_sensor    = Ultrasonic(brick, PORT_4)



# ultra_motor.reset_position(False)

motors = (ultra_motor, left_motor, right_motor)
sensors = (touch_sensor, compass_sensor, sound_sensor, ultra_sensor)
hubo = Robot(motors, sensors)

# front_is_clear()
# will this work?
