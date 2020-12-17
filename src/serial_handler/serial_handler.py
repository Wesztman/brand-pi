import logging, os, threading


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
