import logging, os, threading, queue
from serial import Serial
from robust_serial.utils import open_serial_port


class SerialHandler(threading.Thread):
    def __init__(self, port, in_que, out_que):
        self.port = port
        self.in_que = in_que
        self.out_que = out_que
        # Open serial connection to the slave device
        # TODO(CW,201217): Add wait or try/except if port could not open
        self.slave_device = open_serial_port(
            serial_port=self.port, baudrate=9600, timeout=1
        )
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, daemonic=True)

    def run(self):
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
