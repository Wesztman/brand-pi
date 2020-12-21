#!/usr/bin/env python3

import os, logging, threading, pty, sys, signal, queue
from serial import Serial
from transitions import Machine
from datetime import datetime
from time import sleep
from logging.handlers import RotatingFileHandler
from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_order

# Self defined imports
from robot_state_machine.robot_state_machine import RobotStateMachine
from config_handler.config_handler import GetConfiguration, config_file_listener
from serial_handler.serial_handler import SerialHandler
from teensy_sim.teensy_sim import TeensySim


def signal_handler(sig, frame):
    logging.info("Exiting")
    sys.exit(0)


def main():
    """ Queue declerations """
    # In queue and out queue for serial communication
    ser_in_queue = queue.Queue()
    ser_out_queue = queue.Queue()

    """ State machine decleration """
    # Variables for state enter actions
    current_state = ""
    previous_state = ""

    # Create robot state machine object
    robot = RobotStateMachine()

    """ Config file handling """
    # Initialize config parser
    current_folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_folder, "config.ini")
    get_config = GetConfiguration(config_file)

    # Start config file listener thread
    config_file_listener_thread = threading.Thread(
        target=config_file_listener, args=[config_file], daemon=True
    )
    config_file_listener_thread.start()

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

    """ Serial communication """
    if get_config.as_bool("communication", "teensy_sim_mode"):
        # Create teensy sim object and start thread
        teensy_sim = TeensySim()
        teensy_sim.start()
        slave_port = teensy_sim.get_slave_port()
    else:
        slave_port = get_config.as_string("communication", "teensy_port")
    # Create serial handler object and start thread for the slave device
    slave_device = SerialHandler(slave_port, ser_in_queue, ser_out_queue)
    slave_device.start()
    # Initialize signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Create data set

    """ Main loop start """
    while True:

        current_state = robot.state

        # ======================================================================== #
        if robot.state == "init":

            # Init done, wait for serial device to connect
            if slave_device.connected():
                logging.info("Initialization done")
                robot.init_done()

        # ======================================================================== #
        elif robot.state == "idle":

            if previous_state != robot.state:  # State enter actions, run once
                pass

                """ Check for start button """
                # logging.info("Start button pressed")
                robot.start()

        # ======================================================================== #
        elif robot.state == "working":

            if previous_state != robot.state:  # State enter actions, run once
                pass

            """ Internal working loop """

            # -------------------------------------------------------------------------#
            # Internal Working State: Read Input

            # -------------------------------------------------------------------------#
            # Internal Working State: Data Processing

            # -------------------------------------------------------------------------#
            # Internal Working State: Set Output

            # -------------------------------------------------------------------------#
            # Internal Working State: Cleanup -> Go to Read Input

            """ Check for stop button """
            # logging.info("Stop button pressed")
            # Got to cleanup
            # robot.stop()

        # ======================================================================== #
        elif robot.state == "cleanup":

            if previous_state != robot.state:  # State enter actions, run once
                pass

            # Cleanup

            # Go to Idle
            robot.reset()

        else:
            logging.warning("Unhandled robot state")
            exit(1)

        if current_state == robot.state:
            previous_state = robot.state


if __name__ == "__main__":
    main()