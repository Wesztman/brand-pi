import logging
from transitions import Machine


class RobotStateMachine:
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
            states=RobotStateMachine.states,
            transitions=RobotStateMachine.transitions,
            initial="init",
        )

    def __del__(self):
        logging.info("State machine shutting down")