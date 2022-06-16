# Robot simulation class
# robot joint are simulate as first order inertial object with delay

from robot_spec import *


# Class to simulate robot arm move
class RobotSimulation:
    # class init
    def __init__(self):
        self.x = [0, 0, 0]  # vector of motor position in state space model

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
        for i in range(0, 3):
            x = self.x[i]       # current position
            u = set_angle[i]    # required position
            # check st point position limit and apply in case overflow
            u = self.apply_limits(u)
            self.x[i] = (0.8172 * x + 0.5 * u)   # calculate new x in state space model

    def get_robot_position(self):
        return self.x * 0.3656  # return scaled motor position [deg]
