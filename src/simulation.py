# Robot simulation class
# robot joint are simulate as first order inertial object with delay

from src.robot_spec import *
from threading import Lock


# Class to simulate robot arm move
class RobotSimulation:
    # class init
    def __init__(self):
        self.x = [0, 0, 0]   # vector of motor position in state space model
        self.mutex = Lock()  # Position mutex

    # apply limit to se point value
    def apply_limits(self, u):
        if u > ARM_POSITION_MAX:
            return ARM_POSITION_MAX
        if u < ARM_POSITION_MIN:
            return ARM_POSITION_MIN
        return u

    # Simulate motors moves every 20ms using discrete servo model MG995
    def simulate_motors(self, set_angle):
        # calculate new motor position for each motor
        self.mutex.acquire()
        for i in range(0, 3):
            x = self.x[i]       # current position
            u = set_angle[i]    # required position
            # check st point position limit and apply in case overflow
            u = self.apply_limits(u)
            self.x[i] = (0.8172 * x + 0.5 * u)   # calculate new x in state space model
        self.mutex.release()
        return [x * 0.3656 for x in self.x]  # return scaled motor position [deg]

    # get scaled simulation output
    def get_output(self):
        self.mutex.acquire()
        out = []
        for x in self.x:
            out.append(x * 0.3656)
        self.mutex.release()
        return out  # return scaled motor position [deg]

