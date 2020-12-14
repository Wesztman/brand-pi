#!/usr/bin/env python3

from transitions import Machine
from datetime import datetime
from time import sleep
import logging
from logging.handlers import RotatingFileHandler
import os
import select
from inotify_simple import INotify, flags
import threading

from robot_state_machine.robot_state_machine import RobotStateMachine
from get_configuration.get_configuration import GetConfiguration


def config_file_listener(config_file):
    # Initialize inotify object
    inotify = INotify()
    watch_flags = flags.MODIFY
    wd = inotify.add_watch(config_file, watch_flags)

    while True:
        # Watch config file changes
        readable, _, _ = select.select([inotify], [], [])

        if inotify in readable:
            for event in inotify.read(timeout=0):
                for flag in flags.from_mask(event.mask):
                    logging.info("Config file changed")
                    # Do stuff


def main():
    # Initialize config parser
    current_folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_folder, "config.ini")
    get_config = GetConfiguration(config_file)

    # Create general thread list
    threads = []

    # Initialize config file listener thread
    config_file_listener_thread = threading.Thread(
        target=config_file_listener, args=[config_file]
    )
    threads.append(config_file_listener_thread)
    config_file_listener_thread.start()

    # Create serial object

    # Variables for state enter actions
    current_state = ""
    previous_state = ""

    # Create state machine object
    robot = RobotStateMachine()

    # Initialize logger
    logging.basicConfig(
        level=get_config.as_int("logging", "log_level"),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            RotatingFileHandler("logs/debug.log", maxBytes=1000000, backupCount=5),
            logging.StreamHandler(),
        ],
    )

    # Initialize signal handler

    # MAIN LOOP START #
    while True:

        current_state = robot.state

        # Watch config file changes
        # for event in inotify.read(timeout=0):
        #     for flag in flags.from_mask(event.mask):
        #         print("Config file changed")
        #         # Do stuff

        # Update log level if changed

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