from transitions import Machine
from datetime import datetime
from time import sleep
import logging
from logging.handlers import RotatingFileHandler


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
    # Parse config file
    # Initialize file change notifier on config file

    # Variables for state enter actions
    current_state = ""
    previous_state = ""

    # Create state machine object
    robot = Robot()

    # Initialize logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            RotatingFileHandler("debug.log", maxBytes=1000000, backupCount=5),
            logging.StreamHandler(),
        ],
    )

    # Initialize signal handler

    # MAIN LOOP START #
    while True:

        now_time = datetime.now()
        current_state = robot.state

        # Watch dynamic config changes

        # ======================================================================== #
        if robot.state == "init":

            if previous_state != robot.state:  # State enter actions, run once
                pass

            sleep(1.0)
            robot.init_done()

            # Create data sets

        # ======================================================================== #
        elif robot.state == "idle":

            if previous_state != robot.state:  # State enter actions, run once
                pass

            sleep(1)
            robot.start()

            # Wait for start

            # Go to Working

        # ======================================================================== #
        elif robot.state == "working":

            if previous_state != robot.state:  # State enter actions, run once
                pass

            sleep(1.0)
            robot.stop()

            # INTERNAL WORKING LOOP START #

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

            if previous_state != robot.state:  # State enter actions, run once
                pass

            sleep(1.0)
            robot.reset()

            # Cleanup

            # Go to Idle

        else:
            logging.warning("Unhandled robot state")
            exit(1)

        if current_state == robot.state:
            previous_state = robot.state


if __name__ == "__main__":
    main()