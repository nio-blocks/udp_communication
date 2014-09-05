import binascii
from enum import Enum
from socketserver import ThreadingMixIn, UDPServer, BaseRequestHandler
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.common.signal.base import Signal
from nio.metadata.properties.int import IntProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.select import SelectProperty
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.modules.threading import spawn
from .mixins.collector.collector import Collector


from UDP_general import process_data

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
        #data = self.request[0].strip()
        data = self.request[0]
        #socket = self.request[1]
        #client_addr = self.client_address[0]

        pack = self._parse_packet(data)
        if pack:
            self.server.notifier(*pack)

    def _parse_packet(self, packet):
        return process_data(packet)

@Discoverable(DiscoverableType.block)
class GeneralUDP(Collector, Block):
    """ A Block for reading from a "general" UDP object (data in format `name:type:data`
    - type is according to python struct guidelines """

    host = StringProperty(title="Listener Host", default="127.0.0.1")
    port = IntProperty(title="Listener Port", default=5008)

    def __init__(self):
        super().__init__()
        self._server = None

    def configure(self, context):
        super().configure(context)
        try:
            self._server = ThreadedUDPServer(
                (self.host, self.port),
                GenUDPHandler,
                self._handle_input)
        except Exception as e:
            self._logger.error(
                "Failed to create server - {0} : {1}".format(
                    type(e).__name__, e))

    def start(self):
        super().start()
        if self._server:
            spawn(self._server.serve_forever)
        else:
            self._logger.warning("Server did not exist, so it was not started")

    def stop(self):
        if self._server:
            self._server.shutdown()
        super().stop()

    def _handle_input(self, name, data):
        sig_out = {name: data}
        self.notify_signals([Signal(sig_out)])
        self.notify_signals([Signal(sig_out)])
