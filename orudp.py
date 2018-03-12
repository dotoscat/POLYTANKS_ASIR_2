# orudp
# Copyright (C) 2018  Oscar 'dotoscat' Triano 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.import sched

import struct
import selectors
import socket
from collections import deque

DATA = 1
ACK = 2

header = struct.Struct("!LL")

"""
    UDP is used frequently in networked games by its speed.
    Its only problem is that is not 'reliable', UDP is not oriented
    to connection. It is like send (real world) mails, you do not know if they
    have arrived to its destiny or not.

    This module uses the same analogy from the real world mails to provide mechanism
    to assure that the datagrams (mails) arrive to its destiny and deal with those messages.
    This module do not pretend be a replace for TCP. So better use TCP if does a
    better job.
"""

class Message:
    """
    This class is used internally by :class:`Mailbox`.
    """
    __slots__ = ("id", "data", "tries", "event", "address")
    def __init__(self):
        self.id = None
        self.data = None
        self.tries = None
        self.event = None
        self.address = None

    def reset(self):
        self.id = None
        self.data = None
        self.tries = None
        self.event = None
        self.address = None

class Mailbox:
    DEFAULT_MESSAGES = 256
    def __init__(self, bind=None, blocking=False, protocol=None):
        """
            A mailbox instance will be listening to incoming messages if
            you bind it to an address and set a protocol.

            Arguments:
                bind (tuple): A direction with the ip and the port for serving (listening).
                blocking (bool): This is a blocking connection or not (asyncronous).
                protocol (callable): A callable to attend arriving messages.

            The protocol callback has the following signature:
                protocol(message, address, mailbox)

            Where *message* is the payload, *address* is where the message comes from;
            and *mailbox* is the instance associated to the protocol.
        """
        self._sent = {}
        self._received = {}
        self._id = 0
        self._socket = None
        self._mysched = sched.scheduler()
        self._select = selectors.DefaultSelector()
        self._protocol = protocol
        self._messages = deque([Message() for i in range(self.DEFAULT_MESSAGES)])

        sock = socket.socket(type=socket.SOCK_DGRAM)
        if bind:
            sock.bind(bind)
        sock.setblocking(blocking)
        self._socket = sock
        self._select.register(sock, selectors.EVENT_READ)

    def __del__(self):
        self._select.close()

    def run(self):
        """
        Run the mailbox to attend petitions and manage the status of sent messages.
        """
        events = self._select.select(0)
        for key, mask in events:
            socket = key.fileobj
            data, address = socket.recvfrom(1024)
            if not len(data) >= header.size:
                continue
            id, type = header.unpack_from(data)
            if type == DATA:
                payload = data[header.size:]
                print("You received message with payload:", payload)
                #Do something with the payload
                socket.sendto(header.pack(id, ACK), address)
                if callable(self._protocol):
                    self._protocol(payload, address, self)
                message = self._messages.pop()
                message.id = id
                message.data = payload
                self._received[id] = message
                self._mysched.enter(1, 1, self._remove_message, argument=(id,))
            elif type == ACK:
                if id not in self._sent:
                    continue
                print("{} acknowleged".format(id))
                self._mysched.cancel(self._sent[id].event)
                message = self._sent.pop(id)
                message.reset()
                self._messages.append(message)
        self._mysched.run(False)

    def empty(self):
        """Check if there is not pending messages."""
        return self._mysched.empty()

    def send_message(self, data, time_for_response, tries=None, address=None):
        """
            Arguments:
                data (buffer): Data to send
                time_for_response (float): Time to wait before resend the data
                tries (int): Number of tries. None is no limit.
                address (tuple): The address to send the message.
        """
        buffer = header.pack(self._id, DATA) + data
        message = self._messages.pop()
        message.id = self._id
        message.data = buffer
        message.tries = tries
        message.address = address
        message.event = self._mysched.enter(time_for_response, 1, self._resend, argument=(message, time_for_response))
        self._sent[self._id] = message
        self._id += 1
        return self._send(buffer, address)

    def _send(self, data, address=None):
        if address:
            return self._socket.sendto(data, address)
        else:
            return self._socket.send(data)

    def _resend(self, message, time_for_response):
        if message.tries == 0:
            return
        print("resend after {} seconds:".format(time_for_response), message.data)
        self._send(message.data, message.address)
        self._mysched.enter(time_for_response, 1, self._resend, argument=(message, time_for_response))
        if message.tries:
            message.tries -= 1

    def _remove_message(self, id):
        print("Remove {} from receptor".format(id), self)
        message = self._received.pop(id)
        message.reset()
        self._messages.append(message)