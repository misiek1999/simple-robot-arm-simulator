# Main script to simulate robot arm

import pygame
from src.simulation import RobotSimulation
from src.communication_interface import CommunicationInterface
from time import sleep

if __name__ == '__main__':
    # crate communication object
    interface = CommunicationInterface()
    # run send and receive packet using udp interface
    interface.run()

    set = 10
    sim = RobotSimulation()

    # sleep(1000)
    while True:
        pass

    interface.stop_communication()
    # wait to join communication interface threads
    interface.join()

