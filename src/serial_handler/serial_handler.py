import logging, os, threading, queue, time
from robust_serial import write_order, Order, write_i8
from serial import Serial
from robust_serial.utils import open_serial_port


class SerialHandler(threading.Thread):
    def __init__(self, port, in_que, out_que):
        self.port = port
        self.in_que = in_que
        self.out_que = out_que
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
        # Run serial communication
        while True:
            input = self.in_que.get()
            result = self.serial_command(input)
            self.out_que.put(result)

    def serial_command(self, data):
        self.data = data
        output = self.data + "\r\n"
        output = bytes(output, encoding="utf-8")
        logging.info("Sending command: %s" % output.rstrip())
        self.slave_device.write(output)
        res = b""
        while not res.endswith(b"\r\n"):
            # read the response
            res += self.slave_device.read()
        return res.rstrip()

    def connected(self):
        return self.is_connected