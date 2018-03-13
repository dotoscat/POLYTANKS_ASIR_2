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
        self.message = b'Hello world!'
    
    def run_mailboxes(self):
        while not (self.client.empty() and self.server.empty()):
            self.server.run()
            self.client.run()
        self.server.close()
        self.client.close()

    def manage_message(self, message, address, mailbox):
        self.managed = True
        self.assertEqual(message, self.message, "Message is not equal!")

    def test1_server_bind_client_connect_and_send(self):
        self.server.bind(ADDRESS)
        self.server.set_protocol(self.manage_message)
        self.client.connect(ADDRESS)
        self.client.send_message(self.message, 0.5, 1)
        self.run_mailboxes()
        self.assertTrue(self.managed, "Test1 not passed")

    def test2_server_bind_client_and_send(self):
        self.server.bind(ADDRESS)
        self.server.set_protocol(self.manage_message)
        self.client.send_message(self.message, 0.5, 1, address=ADDRESS)
        self.run_mailboxes()
        self.assertTrue(self.managed, "Test2 not passed")

    def test3_server_bind_and_send_to_client(self):
        self.server.bind(ADDRESS)
        self.client.set_protocol(self.manage_message)
        self.client.connect(ADDRESS)
        client_address = self.client.socket.getsockname()
        self.server.send_message(self.message, 0.5, 1, address=client_address)
        self.run_mailboxes()
        self.assertTrue(self.managed, "Test3 not passed")
