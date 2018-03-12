import sched
import struct
import selectors

DATA = 1
ACK = 2

header = struct.Struct("!LL")

class Message:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.tries = None
        self.event = None
        self.address = None

class Office:
    def __init__(self, socket):
        self._messages = {}
        self._id = 0
        self._socket = socket
        self._mysched = sched.scheduler()
        self._select = selectors.DefaultSelector()
        self._select.register(socket, selectors.EVENT_READ, self._recv)

    def __del__(self):
        self._select.close()

    def send_message(self, data, time_for_response, tries=None, address=None):
        buffer = header.pack(self._id, DATA) + data
        message = Message(self._id, buffer) 
        message.tries = tries
        message.address = address
        message.event = self._mysched.enter(time_for_response, 1, self._resend, argument=(message, time_for_response))
        self._messages[self._id] = message
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
        print("resend after {} seconds".format(time_for_response))
        self._send(message.data, message.address)
        print("resend", message.data)
        self._mysched.enter(time_for_response, 1, self._resend, argument=(message, time_for_response))
        if message.tries:
            message.tries -= 1

    def _recv(self, socket):
        pass

    def run(self):
        events = self._select.select(0)
        for key, mask in events:
            socket = key.fileobj
            data, address = socket.recvfrom(1024)
            if not len(data) >= header.size:
                continue
            print("len", len(data))
            id, type = header.unpack_from(data)
            if type == DATA:
                payload = data[header.size:]
                print("You received message with payload:", payload)
                #Do something with the payload
                socket.sendto(header.pack(id, ACK), address)
            elif type == ACK:
                if id not in self._messages:
                    continue
                print("{} acknowleged".format(id))
                self._mysched.cancel(self._messages[id].event)
                del self._messages[id]
        self._mysched.run(False)

    def empty(self):
        return self._mysched.empty()
