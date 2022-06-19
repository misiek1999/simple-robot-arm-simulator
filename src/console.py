from threading import Thread


# class to communicate with console
class ConsoleInterface:
    def __init__(self):
        self.close_program_flag = False  #flag of closing program
        # create and launch console thread
        self.console_thread = Thread(target=self.console_interface)
        self.console_thread.start()

    # read data from console
    def console_interface(self):
        # wait to input [c] character
        print('Press [c] to close program')
        user_input = ' '
        while user_input[0] != 'c':
            user_input = input()
        self.close_program_flag = True

    # get program state
    def get_program_state(self):
        return self.close_program_flag
