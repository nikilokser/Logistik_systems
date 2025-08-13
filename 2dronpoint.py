import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
from clover.srv import SetLEDEffect
import pigpio
from tqdm import tqdm

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)

pi = pigpio.pi()

pi.set_mode(12, pigpio.OUTPUT)


def navigate_wait(x=0.0, y=0.0, z=0.0, yaw=float('nan'), speed=1, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


navigate_wait(x=0, y=0, z=1.5, frame_id='body', auto_arm=True)
set_effect(effect='blink', r=0, g=0, b=200)
navigate_wait(x=3, y=4, z=2.2, frame_id='aruco_map')
land()
rospy.sleep(2)
land()
rospy.sleep(2)
land()
rospy.sleep(2)
land()
rospy.sleep(2)

set_effect(effect="blink", r=200, g=0, b=0)
pi.set_servo_pulsewidth(12, 2000)
rospy.sleep(1.5)

print("Charging")
set_effect(effect='rainbow')
for _ in tqdm(range(112)):
    rospy.sleep(1)
print("Charged")
navigate_wait(x=0, y=0, z=1.5, frame_id='body', auto_arm=True)
set_effect(r=0, g=0, b=200)
navigate_wait(x=3.3, y=1, z=1.5, frame_id='aruco_map')
land()
rospy.sleep(2)
land()
rospy.sleep(3)
land()
rospy.sleep(2)