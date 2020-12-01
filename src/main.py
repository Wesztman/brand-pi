from transitions import Machine, State
from datetime import datetime
from time import sleep

# import enum


class Robot(object):
    # Main robot states
    states = ["init", "idle", "working", "cleanup"]

    # Available transitions
    transitions = [
        {"trigger": "init_done", "source": "init", "dest": "idle"},
        {"trigger": "start", "source": "idle", "dest": "working"},
        {"trigger": "stop", "source": "working", "dest": "cleanup"},
        {"trigger": "reset", "source": "cleanup", "dest": "idle"},
    ]

    def __init__(self):

        # Initialize state machine
        self.machine = Machine(
            model=self,
            states=Robot.states,
            transitions=Robot.transitions,
            initial="init",
        )


def main():
    now_time = datetime.now()
    print(now_time.isoformat())

    # Variables for state enter actions
    current_state = ""
    previous_state = ""

    # Create state machine object
    robot = Robot()

    # Initialize logger
    # Initialize signal handler
    # Parse config file
    # Initialize file change notifier on config file

    # MAIN LOOP START #
    while True:

        current_state = robot.state

        # Watch dynamic config changes

        # ======================================================================== #
        if robot.state == "init":

            if previous_state != robot.state:
                print("init")

            sleep(1)
            robot.init_done()

            # Create data sets

        # ======================================================================== #
        elif robot.state == "idle":

            if previous_state != robot.state:
                print("idle")

            sleep(1)
            robot.start()

            # Wait for start

            # Go to Working

        # ======================================================================== #
        elif robot.state == "working":

            if previous_state != robot.state:
                print("working")

            sleep(1)
            robot.stop()

            # Loop working states while active #

            # -------------------------------------------------------------------------#
            # Internal Working State: Read Input

            # -------------------------------------------------------------------------#
            # Internal Working State: Data Processing

            # -------------------------------------------------------------------------#
            # Internal Working State: Set Output

            # -------------------------------------------------------------------------#
            # Internal Working State: Cleanup -> Go to Read Input

            # Go to Cleanup

        # ======================================================================== #
        elif robot.state == "cleanup":

            if previous_state != robot.state:
                print("cleanup")

            sleep(1)
            robot.reset()

            # Cleanup

            # Go to Idle

        else:
            print("Unhandled robot state")
            exit(1)

        if current_state == robot.state:
            previous_state = robot.state


if __name__ == "__main__":
    main()