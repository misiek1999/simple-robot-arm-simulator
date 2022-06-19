# Main script to simulate robot arm
from src.render_robot_arm import SimpleRobotRender


if __name__ == '__main__':
    # create robot render object
    render = SimpleRobotRender()
    # run robot render until get program stop signal
    render.run()
