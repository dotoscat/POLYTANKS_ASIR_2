#/usr/bin/env python
import asyncio
import signal
from polytanks import protocol
signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = ("127.0.0.1", 1337)

class Player:
    pass

class ServerProtocolMixin(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("Connection made", transport.get_extra_info("peername"))

    def data_received(self, data):
        print("data_received", data, "from", self.transport.get_extra_info("peername"))
        self.transport.close()
        print("clients", self.clients)

    def connection_lost(self, exc):
        if not exc:
            print("Connection closed normally")
        else:
            print("error", exc)

class Server(ServerProtocolMixin):
    def __init__(self, host=HOST):
        self.loop = asyncio.get_event_loop()
        self.server_coro = self.loop.create_server(lambda: self, *host)
        self.server = self.loop.run_until_complete(self.server_coro)
        self.clients = {}

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.loop.close()

if __name__ == "__main__":
    print("Hola mundo")
    server = Server()
    server.run()
