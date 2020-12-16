#!/usr/bin/env python3

import os, logging, threading, pty
from serial import Serial
from transitions import Machine
from datetime import datetime
from time import sleep
from logging.handlers import RotatingFileHandler
from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_order
from robust_serial.utils import open_serial_port


from robot_state_machine.robot_state_machine import RobotStateMachine
from config_handler.config_handler import GetConfiguration, config_file_listener
from test_serial.test_serial import test_serial


def serial_listener(port):
    while True:
        res = b""
        while not res.endswith(b"\r\n"):
            # Keep reading one byte at a time until we have a full line
            res += os.read(port, 1)
        logging.info("command: %s" % res)

        # Write back the response
        if res == b"QPGS\r\n":
            os.write(port, b"correct result\r\n")
        else:
            os.write(port, b"I dont understand\r\n")


def main():
    """ General declerations """
    # Create general thread list
    threads = []

    # Variables for state enter actions
    current_state = ""
    previous_state = ""

    # Create state machine object
    robot = RobotStateMachine()

    """ Config file handling """
    # Initialize config parser
    current_folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_folder, "config.ini")
    get_config = GetConfiguration(config_file)

    # Initialize config file listener thread
    config_file_listener_thread = threading.Thread(
        target=config_file_listener, args=[config_file]
    )
    threads.append(config_file_listener_thread)
    config_file_listener_thread.start()

    """ Serial communication """
    # Create pseudoterminals for serial testing
    master, slave = pty.openpty()
    slave_name = os.ttyname(slave)

    # Initialize serial listener thread
    serial_listener_thread = threading.Thread(target=serial_listener, args=[master])
    threads.append(serial_listener_thread)
    serial_listener_thread.start()

    # Open serial connection to the slave
    ser = Serial(slave_name, 9600, timeout=1)

    # Write

    """ Logging """
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

    """ Main loop start """
    while True:

        current_state = robot.state

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

            """ Internal working loop """

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