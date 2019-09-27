import zmq
import logging
import time
import pickle


class Ground:

    _port, _addr = 0, ""
    _connected = False
    _connect_timeout = 0
    _recv_timeout = 0
    retries = 10
    package = {}
    frame = 0x00

    def __init__(self):
        ctx = zmq.Context()
        self.soc = ctx.socket(zmq.PAIR)
        self.soc.setsockopt(zmq.SNDTIMEO, 500)
        self.soc.setsockopt(zmq.RCVTIMEO, 500)

        self.logger = logging

    def connect(self, address, port):
        while True:
            try:
                self.soc.connect("tcp://{addr}:{port}".format(addr=address, port=port))
                boot = self.soc.recv().decode("utf-8")
                if not boot == "SIGNAL_BOOT":
                    self._connect_timeout += 1
                    if self._connect_timeout >= self.retries:
                        self.logger.critical("Cannot get boot signal within retries. Breaking...")
                        return
                    self.logger.error("Invalid boot signal: " + boot)
                    continue
                self.soc.send(b"BOOT_CONFIRM")
                self.logger.info("Connection established")
                return
            except Exception as exc:
                self.logger.info("Waiting UAV: {exc}".format(exc=exc))
                time.sleep(1)
                continue


    def recv(self):
        while True:
            if self._recv_timeout >= self.retries:
                self.logger.critical("Cannot get frame within retries")
                self._recv_timeout = 0
                return
            try:
                self.frame = pickle.loads(self.soc.recv())
                self.package = pickle.loads(self.soc.recv())
                return
            except Exception as exc:
                self.logger.error(exc)
                self._recv_timeout += 1

