import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from math import *
from src.console import ConsoleInterface
from src.communication_interface import CommunicationInterface


# class to render robot arm
class SimpleRobotRender:
    # init class
    def __init__(self):
        matplotlib.use('TkAgg')
        self.joint_pos = [0, 0, 0]  # set start robot position
        self.arm_len_list = [12, 10, 10]
        self.fig = plt.figure()
        plt.ion()
        # create and launch console communication thread
        self.console_comm = ConsoleInterface()
        # crate communication object
        self.interface = CommunicationInterface()
        # run send and receive packet using udp interface
        self.interface.run()

    # launch new thread to visualize robot move
    def run(self):
        # create new window with robot visualization
        ax = self.fig.add_subplot(111, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        while not self.console_comm.get_program_state():
            # read current joint position
            joint_pos = self.interface.get_position()
            joint_cart_pos = self.calculate_cartesian_robot_position(joint_pos)
            # draw robot arm
            for joint in joint_cart_pos:
                ax.scatter(joint[0], joint[1], joint[2])
            # display robot arm
            plt.show()
            # wait 20ms to next iteration
            plt.pause(0.02)

        # close other threads
        self.interface.stop_communication()
        self.interface.join()

    # set robot joint position
    def set_robot_position(self, pos):
        for i in len(self.joint_pos):
            self.joint_pos[i] = pos[i]

    def calculate_cartesian_robot_position(self, raw_joint_pos):
        # separate robot position and length
        joint_1_angle = raw_joint_pos[0]
        joint_2_angle = raw_joint_pos[1]
        joint_3_angle = raw_joint_pos[2]
        ARM_1_LENGTH = self.arm_len_list[0]
        ARM_2_LENGTH = self.arm_len_list[1]
        ARM_3_LENGTH = self.arm_len_list[2]

        # calculate cartesian position for joint 1 pos
        cartesian_position_x = 0
        cartesian_position_y = 0
        cartesian_position_z = ARM_1_LENGTH
        joint_1_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        # calculate cartesian position for joint 2 pos
        dx = cos(joint_2_angle) * ARM_2_LENGTH
        dy = sin(joint_2_angle) * ARM_2_LENGTH
        cartesian_position_x = cos(joint_1_angle) * dx
        cartesian_position_y = sin(joint_1_angle) * dx
        cartesian_position_z = ARM_1_LENGTH + dy
        joint_2_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        # calculate cartesian position for joint 3 pos
        dx = cos(joint_2_angle) * ARM_2_LENGTH + cos(joint_2_angle + joint_3_angle) * ARM_3_LENGTH
        dy = sin(joint_2_angle) * ARM_2_LENGTH + sin(joint_2_angle + joint_3_angle) * ARM_3_LENGTH
        cartesian_position_x = cos(joint_1_angle) * dx
        cartesian_position_y = sin(joint_1_angle) * dx
        cartesian_position_z = ARM_1_LENGTH + dy
        joint_3_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        return [joint_1_cart, joint_2_cart, joint_3_cart]
