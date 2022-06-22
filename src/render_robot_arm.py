import matplotlib.pyplot as plt
import matplotlib
import sys
import numpy as np
from math import *
from src.communication_interface import CommunicationInterface
from mpl_toolkits import mplot3d


# class to render robot arm
class SimpleRobotRender:
    # init class
    def __init__(self):
        matplotlib.use('TkAgg')
        # init class variable
        self.close_program = False  # close program flag
        self.joint_pos = [0, 0, 0]  # set start robot position
        self.arm_len_list = [12, 10, 10]  # length of robot arm
        self.fig = plt.figure()
        # crate communication object
        self.interface = CommunicationInterface()
        # keyboard and close windows event handle
        self.fig.canvas.mpl_connect('close_event', self.windows_close)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)
        # run send and receive packet using udp interface
        self.interface.run()

    # launch new thread to visualize robot move
    def run(self):
        plt.rcParams["figure.autolayout"] = True
        # create new window with robot visualization
        ax = self.fig.add_subplot(projection='3d')
        # render robot
        while not self.close_program:
            # clear display
            plt.cla()
            # set axis name
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            # set axis limit
            ax.set_xlim3d(-20, 20)
            ax.set_ylim3d(-20, 20)
            ax.set_zlim3d(0, 40)
            # read current joint position
            joint_pos = self.interface.get_position()
            joint_cart_pos = self.calculate_cartesian_robot_position(joint_pos)
            # color list
            color_list = ['b', 'y', 'g']
            # draw point connection line
            for i in range(0, 3):
                line_x = np.linspace(joint_cart_pos[i][0], joint_cart_pos[i + 1][0])
                line_y = np.linspace(joint_cart_pos[i][1], joint_cart_pos[i + 1][1])
                line_z = np.linspace(joint_cart_pos[i][2], joint_cart_pos[i + 1][2])
                ax.scatter(line_x, line_y, line_z, color=color_list[i])

            # draw robot arm joint points
            for joint in joint_cart_pos:
                ax.scatter(joint[0], joint[1], joint[2], color='r')

            # display manipulator position
            position_str = "Manipulator position \n: x: {:.2f}, y: {:.2f}, z: {:.2f}".format(joint_cart_pos[3][0],
                                                                                             joint_cart_pos[3][1],
                                                                                             joint_cart_pos[3][2])
            ax.set_title(position_str)
            if not self.close_program:
                # display robot arm
                plt.show(block=False)
                # wait 20ms to next iteration
                plt.pause(0.02)

        # close other threads
        self.interface.stop_communication()
        self.interface.join()

    # set robot joint position
    def set_robot_position(self, pos):
        for i in len(self.joint_pos):
            self.joint_pos[i] = pos[i]

    # calculate cartesian position of each joint
    def calculate_cartesian_robot_position(self, raw_joint_pos):
        # separate robot position and length
        joint_1_angle = raw_joint_pos[0]
        joint_2_angle = raw_joint_pos[1]
        joint_3_angle = raw_joint_pos[2]
        ARM_1_LENGTH = self.arm_len_list[0]
        ARM_2_LENGTH = self.arm_len_list[1]
        ARM_3_LENGTH = self.arm_len_list[2]

        joint_0_cart = [0, 0, 0]  # robot base position

        # calculate cartesian position for joint 1 pos
        cartesian_position_x = 0
        cartesian_position_y = 0
        cartesian_position_z = ARM_1_LENGTH
        joint_1_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        # calculate cartesian position for joint 2 pos
        dx = cos(radians(joint_2_angle)) * ARM_2_LENGTH
        dy = sin(radians(joint_2_angle)) * ARM_2_LENGTH
        cartesian_position_x = cos(radians(joint_1_angle)) * dx
        cartesian_position_y = sin(radians(joint_1_angle)) * dx
        cartesian_position_z = ARM_1_LENGTH + dy
        joint_2_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        # calculate cartesian position for joint 3 pos
        dx = cos(radians(joint_2_angle)) * ARM_2_LENGTH + cos(radians(joint_2_angle + joint_3_angle)) * ARM_3_LENGTH
        dy = sin(radians(joint_2_angle)) * ARM_2_LENGTH + sin(radians(joint_2_angle + joint_3_angle)) * ARM_3_LENGTH
        cartesian_position_x = cos(radians(joint_1_angle)) * dx
        cartesian_position_y = sin(radians(joint_1_angle)) * dx
        cartesian_position_z = ARM_1_LENGTH + dy
        joint_3_cart = [cartesian_position_x, cartesian_position_y, cartesian_position_z]

        return [joint_0_cart, joint_1_cart, joint_2_cart, joint_3_cart]

    # windows close event handler
    def windows_close(self, event):
        self.close_program = True
        self.interface.stop_communication()
        self.interface.join()
        exit(0)

    # key press event handler
    def key_press(self, event):
        sys.stdout.flush()
        if event.key == 'c':
            self.close_program = True
