from nio.testing.block_test_case import NIOBlockTestCase
from ..udp_receive import UDPReceive


class TestUDPReceive(NIOBlockTestCase):

    def test_block(self):
        blk = UDPReceive()
        self.configure_block(blk, {
        })
        blk.start()
        blk.stop()
