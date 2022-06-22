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
    def apply_limits(self, pos_list):
        for itr in range(0,3):
            if pos_list[itr] > ARM_POSITION_LIMIT[itr][1]:  # max limit reach
                pos_list[itr] = ARM_POSITION_LIMIT[itr][1]
            if pos_list[itr] < ARM_POSITION_LIMIT[itr][0]:  # min limit reach
                pos_list[itr] = ARM_POSITION_LIMIT[itr][0]

    # Simulate motors moves every 20ms using discrete servo model MG995
    def simulate_motors(self, set_angle):
        # calculate new motor position for each motor
        self.mutex.acquire()
        self.apply_limits(set_angle)    # check st point position limit and apply in case overflow
        for i in range(0, 3):
            x = self.x[i]       # current position
            u = set_angle[i]    # required position
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

