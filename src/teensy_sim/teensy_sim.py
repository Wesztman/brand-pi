import logging, os, threading, pty


class TeensySim(threading.Thread):
    def __init__(self):
        # Create pseudoterminals for serial testing
        master, slave = pty.openpty()
        self.master_name = master
        self.slave_name = os.ttyname(slave)
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, daemonic=True)

    def run(self):
        while True:
            res = b""
            while not res.endswith(b"\r\n"):
                # Keep reading one byte at a time until we have a full line
                res += os.read(self.master_name, 1)

            res = res.rstrip()
            logging.info("*Teensy sim* Command received: %s" % res)

            # Write back the response
            if res == b"right_distance":
                os.write(self.master_name, b"*Teensy sim* right_distance: 100\r\n")
            elif res == b"left_distance":
                os.write(self.master_name, b"*Teensy sim* left_distance: 50\r\n")
            else:
                os.write(self.master_name, b"*Teensy sim* Incorrect command\r\n")

    def get_slave_port(self):
        return self.slave_name