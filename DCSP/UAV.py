import zmq
import logging
import time
import pickle

class UAV:

    _port = 0
    _timeout_counter = 0
    _updated = False
    retries = 10

    package = {}
    frame = 0x00

    def __init__(self, port):
        ctx = zmq.Context()
        self.soc = ctx.socket(zmq.PAIR)
        self.soc.setsockopt(zmq.SNDTIMEO, 500)
        self.soc.setsockopt(zmq.RCVTIMEO, 500)
        self.soc.bind("tcp://*:{port}".format(port=port))

        self.logger = logging
        self._port = port

        while True:
            try:
                self.soc.send(b"SIGNAL_BOOT")
                confirm = self.soc.recv().decode("utf-8")
                if confirm == "BOOT_CONFIRM":
                    break
                self.logger.error("Connection confirmation is not valid: {inv_data}".format(inv_data=confirm))
                print("Connection confirmation is not valid: {inv_data}".format(inv_data=confirm))
            except Exception as exc:
                self.logger.info("Waiting ground: {exc}".format(exc=exc))
                print("Waiting ground: {exc}".format(exc=exc))
                time.sleep(.2)



    def wrap_package(self, **data):
        temp_dict = {}
        for key, value in data.items():
            temp_dict[key] = value
        self.package = pickle.dumps(temp_dict)

    def wrap_frame(self, frame):
        self.frame = pickle.dumps(frame)
        self._updated = True

    def send(self):
        if not self._updated:
            logging.error("Send command called before updating frame.")
            return

        while True:
            try:
                self.soc.send(self.frame)
                self.soc.send(self.package)
                self._updated = False
                return True
            except Exception as exc:
                if self._timeout_counter >= self.retries:
                    self.logger.error("Encountered as many timeouts as retries. ({ret})".format(ret=self.retries))
                    return False
                self._timeout_counter += 1
                self.logger.error(str(exc))
                continue


