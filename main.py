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
    # for i in range(0, 50*20):
    #     print(sim.simulate_motors([set, set, set])[0])

    sleep(100)
    interface.stop_communication()
    # wait to join communication interface threads
    interface.join()

