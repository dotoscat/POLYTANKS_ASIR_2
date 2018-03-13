import unittest

import time
import signal
import orudp

signal.signal(signal.SIGINT, signal.SIG_DFL)

ADDRESS = ('127.0.0.1', 1337)

class TestOrudpAsync(unittest.TestCase):
    def setUp(self):
        self.server = orudp.Mailbox()
        self.client = orudp.Mailbox()
        self.managed = False
    
    def run_mailboxes(self):
        while not (self.client.empty() and self.server.empty()):
            self.server.run()
            self.client.run()

    def manage_message(self, message, address, mailbox):
        self.managed = True

    def test1_server_bind_client_connect_and_send(self):
        self.server.bind(ADDRESS)
        self.server.set_protocol(self.manage_message)
        self.client.connect(ADDRESS)
        self.client.send_message(b'Hello', 0.5, 1)
        self.run_mailboxes()
        self.assertTrue(self.managed, "Test1 not passed")
