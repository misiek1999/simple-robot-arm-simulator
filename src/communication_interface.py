# communication with robot controller using UDP socket
import ctypes
import socket
import struct
from ctypes import *
from threading import Thread, Lock
from time import sleep
from src.simulation import RobotSimulation

# Const socket parameters
UDP_IP = "127.0.0.1"
UDP_RECEIVE_PORT = 22223
UDP_SEND_PORT = 22222


# Class to communicate with robot controller
class CommunicationInterface:
    # force variable type
    digital_in: ctypes.c_uint8
    digital_out: ctypes.c_uint8
    # Init class
    def __init__(self):
        self.stop_program = False
        self.rec_thread = Thread(target=self.receive_data)
        self.send_thread = Thread(target=self.receive_data)
        self.sim = RobotSimulation()    # Robot simulation class
        self.digital_in = 0     # Init digital input to 0
        self.digital_out = 0    # Init digital output to 0
        self.set_point_position = [0, 0, 0]
        self.mutex = Lock()

    # Method to stop udp communication
    def stop_communication(self):
        self.stop_program = True

    # Method to launch receive and send data packet in new threads
    def run(self):
        # run threads to receive and send udp packet
        self.rec_thread.start()
        # self.send_thread.start()

    # Method to join both class threads
    def join(self):
        self.rec_thread.join()
        # self.send_thread.join()

    # receive packet using udp socket
    def receive_data(self):
        # init receive udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_RECEIVE_PORT))
        sock.settimeout(1)  # set 1 s timeout for receive socket

        # read data until receive stop signal
        while not self.stop_program:
            # try to receive data with 1s timeout
            try:
                raw_data, addr = sock.recvfrom(1024)    # oversize receive buffer
                rec_data = struct.unpack('fffB', raw_data)
                self.mutex.acquire()
                self.set_point_position[0] = rec_data[0]
                self.set_point_position[1] = rec_data[1]
                self.set_point_position[2] = rec_data[2]
                self.digital_in = rec_data[3]
                self.mutex.release()
                print(rec_data)
            except:     # if receive is impossible do nothing
                pass

        # close socket
        sock.close()

    # send packet using udp socket
    def send_data(self):
        # init receive udp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_SEND_PORT))
        # send packet every 20ms
        while not self.stop_program:
            # get actual set point position
            self.mutex.acquire()
            set_point = self.set_point_position
            digital = self.digital_out
            self.mutex.release()
            # simulate robot movement
            pos = self.sim.simulate_motors(set_point)
            # send packet using udp
            packet = sock.send(struct.pack('fffB', pos, digital))
            sock.send(packet)
            sleep(0.02)  #wait 20ms to send next packet

        # close socket
        sock.close()

    # get current robot position
    def get_position(self):
        return self.sim.get_output()