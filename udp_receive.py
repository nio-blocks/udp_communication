from socketserver import ThreadingMixIn, UDPServer, BaseRequestHandler

from nio import GeneratorBlock
from nio.signal.base import Signal
from nio.properties import IntProperty, StringProperty, VersionProperty
from nio.util.threading.spawn import spawn
from nio.block.mixins.collector.collector import Collector

from .udp_general import process_data


class ThreadedUDPServer(ThreadingMixIn, UDPServer):
    def __init__(self, server_address, handler_class, notifier):
        super().__init__(server_address, handler_class)
        self.notifier = notifier


class GenUDPHandler(BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0]

        pack = self._parse_packet(data)
        if pack:
            self.server.notifier(pack)

    def _parse_packet(self, packet):
        return process_data(packet)


class UDPReceive(Collector, GeneratorBlock):
    """ Reads from a "general" UDP object

    data in format `name:type:data`
    - type is according to python struct guidelines
    """

    host = StringProperty(title="Listener Host", default="127.0.0.1")
    port = IntProperty(title="Listener Port", default=5008)
    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._server = None

    def configure(self, context):
        super().configure(context)
        try:
            self._server = ThreadedUDPServer(
                (self.host(), self.port()),
                GenUDPHandler,
                self._handle_input)
        except Exception as e:
            self.logger.error(
                "Failed to create server - {0} : {1}".format(
                    type(e).__name__, e))

    def start(self):
        super().start()
        if self._server:
            spawn(self._server.serve_forever)
        else:
            self.logger.warning("Server did not exist, so it was not started")

    def stop(self):
        if self._server:
            self._server.shutdown()
        super().stop()

    def _handle_input(self, signal):
        self.notify_signals([Signal(signal)])
