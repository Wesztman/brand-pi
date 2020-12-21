import logging, os, threading, queue, time
from robust_serial import write_order, Order, write_i8
from serial import Serial
from robust_serial.utils import open_serial_port, CustomQueue
from robust_serial.threads import CommandThread, ListenerThread


class SerialHandler(threading.Thread):
    def __init__(self, port):
        self.port = port
        self.is_connected = False

        # Create serial communication object
        try:
            self.slave_device = open_serial_port(
                serial_port=self.port, baudrate=9600, timeout=1
            )
        except Exception as e:
            raise e
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, daemonic=True)

    def __del__(self):
        logging.info("Serial handler shutting down")

    def run(self):
        # Initialize communication with serial device
        while not self.is_connected:
            logging.info("Waiting for serial device on port {}...".format(self.port))
            write_order(self.slave_device, Order.HELLO)
            bytes_array = bytearray(self.slave_device.read(1))
            if not bytes_array:
                time.sleep(2)
                continue
            byte = bytes_array[0]
            if byte == Order.HELLO.value or byte == Order.ALREADY_CONNECTED.value:
                self.is_connected = True
        logging.info("Connected to serial device on port {}".format(self.port))

        # Create Command queue for sending orders
        self.command_queue = CustomQueue(2)
        # Number of messages we can send to the serial device without receiving an acknowledgment
        n_messages_allowed = 3
        self.n_received_semaphore = threading.Semaphore(n_messages_allowed)
        # Lock for accessing serial file (to avoid reading and writing at the same time)
        serial_lock = threading.Lock()

        # Event to notify threads that they should terminate
        self.exit_event = threading.Event()

        logging.info("Starting serial communication threads")
        # Threads for serial communication
        threads = [
            CommandThread(
                self.slave_device,
                self.command_queue,
                self.exit_event,
                self.n_received_semaphore,
                serial_lock,
            ),
            ListenerThread(
                self.slave_device,
                self.exit_event,
                self.n_received_semaphore,
                serial_lock,
            ),
        ]
        # Start threads
        for t in threads:
            t.start()

    def connected(self):
        return self.is_connected

    def send_command(self, Order, value):
        logging.debug(
            "Serial handler sending command {} with value {} to device {}".format(
                Order, value, self.port
            )
        )
        self.command_queue.put((Order, value))

    def get_file_handler(self):
        return self.slave_device
