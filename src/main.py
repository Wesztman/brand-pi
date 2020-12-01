from transitions import Machine
from datetime import datetime


class Robot(object):
    # Main robot states
    states = ["init", "idle", "working", "cleanup"]

    # Available state transitions
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

    # Create state machine object
    # Initialize logger
    # Initialize signal handler
    # Parse config file
    # Initialize file change notifier on config file

    # MAIN LOOP START #

    # Watch dynamic config changes

    # ----------------#
    # -- Init State --#
    # ----------------#

    # Create data sets

    # ----------------#
    # -- Idle State --#
    # ----------------#

    # Wait for start

    # Go to Working

    # -------------------#
    # -- Working State --#
    # -------------------#

    # Loop working states while active #
    # ----------------------------------#

    # Internal Working State: Read Input

    # Internal Working State: Data Processing

    # Internal Working State: Set Output

    # Internal Working State: Cleanup -> Go to Read Input
    # ----------------------------------#

    # Go to Cleanup

    # -------------------#
    # -- Cleanup State --#
    # -------------------#

    # Cleanup

    # Go to Idle


if __name__ == "__main__":
    main()