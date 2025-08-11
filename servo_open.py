#sudo systemctl enable pigpiod.service

import time
import pigpio
import rospy
from clover.srv import SetLEDEffect


set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
pi = pigpio.pi()

pi.set_mode(13, pigpio.OUTPUT)

set_effect(r=200, g=0, b=0)

pi.set_servo_pulsewidth(13, 2000)

time.sleep(2)