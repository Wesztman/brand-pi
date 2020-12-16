import logging, os


def teensy_sim(port):
    while True:
        res = b""
        while not res.endswith(b"\r\n"):
            # Keep reading one byte at a time until we have a full line
            res += os.read(port, 1)

        res = res.rstrip()
        logging.info("*Teensy sim* Command received: %s" % res)

        # Write back the response
        if res == b"right_distance":
            os.write(port, b"*Teensy sim* 100\r\n")
        elif res == b"left_distance":
            os.write(port, b"*Teensy sim* 50\r\n")
        else:
            os.write(port, b"*Teensy sim* Incorrect command\r\n")


def serial_command(ser, data):
    output = data + "\r\n"
    output = bytes(output, encoding="utf-8")
    logging.info("Sending command: %s" % output.rstrip())
    ser.write(output)
    res = b""
    while not res.endswith(b"\r\n"):
        # read the response
        res += ser.read()
    return res.rstrip()
