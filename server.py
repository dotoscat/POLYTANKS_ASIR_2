#/usr/bin/env python
import sys
import weakref
import asyncio
import signal
from polytanks import protocol
signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = ("127.0.0.1", 1337)

class Player:
    pass

class ServerProtocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made", transport.get_extra_info("peername"))

    def data_received(self, data):
        peername = self.transport.get_extra_info("peername")
        print("data_received", data, "from", self.transport.get_extra_info("peername"))
        command = data.from_bytes(data, sys.byteorder)
        if command == protocol.CONNECT:
            if self.server.add_client(peername):
                self.transport.write(b"OK")
            else:
                self.transport.write(b"NO")
        self.transport.close()
        print("clients", self.server.clients)

    def connection_lost(self, exc):
        if not exc:
            print("Connection closed normally")
        else:
            print("error", exc)

class Server:
    def __init__(self, max_n_players, host=HOST):
        self.loop = asyncio.get_event_loop()
        self.server_coro = self.loop.create_server(
            lambda: ServerProtocol(weakref.proxy(self)), *host)
        self.server = self.loop.run_until_complete(self.server_coro)
        self.clients = {}
        self.max_n_players = max_n_players

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())
            self.loop.close()
    
    @property
    def is_full(self):
        return len(self.clients) >= self.max_n_players

    def add_client(self, address):
        if self.is_full:
            return False
        self.clients[address] = Player()
        return True

    def remove_client(self, address):
        if not address in self.clients:
            return False
        del self.clients[address]
        return True

if __name__ == "__main__":
    print("Hola mundo")
    server = Server(2)
    server.run()
