import logging, os, threading, pty, time
from robust_serial import write_order, read_order, Order, read_i8
from robust_serial.utils import open_serial_port


class TeensySim(threading.Thread):
    def __init__(self):
        # Create pseudoterminals for serial testing
        master, slave = pty.openpty()
        self.master = master
        self.slave_name = os.ttyname(slave)
        logging.info("*TEENSY SIM* Started")
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, daemonic=True)

    def __del__(self):
        logging.info("Teensy sim shutting down")

    def run(self):
        self.is_connected = False

        while True:
            if not self.is_connected:
                os.write(self.master, bytes([Order.HELLO.value]))

            self.get_serial_message()

    def get_slave_port(self):
        return self.slave_name

    def get_serial_message(self):
        bytes_array = bytearray(os.read(self.master, 1))
        received_order = bytes_array[0]

        if received_order == Order.HELLO.value:
            if not self.is_connected:
                self.is_connected = True
                os.write(self.master, bytes([Order.HELLO.value]))
            else:
                os.write(self.master, bytes([Order.ALREADY_CONNECTED.value]))
        elif received_order == Order.ALREADY_CONNECTED.value:
            self.is_connected = True
        else:
            if received_order == Order.STOP.value:
                logging.info("*TEENSY SIM* Received order to stop")
            elif received_order == Order.MOTOR.value:
                motor_speed = os.read(self.master, 1)
                logging.info(
                    "*TEENSY SIM* Received motor order with value {}".format(
                        ord(motor_speed.decode("utf-8"))
                    )
                )
            elif received_order == Order.SERVO.value:
                servo_angle = os.read(self.master, 1)
                logging.info(
                    "*TEENSY SIM* Received servo order with value {}".format(
                        ord(servo_angle.decode("utf-8"))
                    )
                )
            else:
                os.write(self.master, bytes([Order.ERROR.value]))

        os.write(self.master, bytes([Order.RECEIVED.value]))