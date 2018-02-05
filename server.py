#/usr/bin/env python
import asyncio
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = ("127.0.0.1", 1337)

class Server:
    def __init__(self, host=HOST):
        self.loop = asyncio.get_event_loop()

    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

if __name__ == "__main__":
    print("Hola mundo")
    server = Server()
    server.run()
