# Main script to simulate robot arm
from src.render_robot_arm import SimpleRobotRender


if __name__ == '__main__':
    # Display keyboard instruction
    print('Welcome to robot simulator')
    print('To close program press [c] in program window')
    # create robot render object
    render = SimpleRobotRender()
    # run robot render and simulation
    render.run()
