#/usr/bin/env python
import sys
import os
import signal
import server.server as server
Server = server.Server
signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.path.insert(0, os.path.abspath(__package__))

if __name__ == "__main__":
    HOST = ("127.0.0.1", 1337)
    server = Server(2, HOST)
    server.run()
