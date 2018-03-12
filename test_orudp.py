import unittest

import selectors
import time
import signal
import orudp
import socket

signal.signal(signal.SIGINT, signal.SIG_DFL)

ADDRESS = ('127.0.0.1', 1337)

message = b'Hola mundo'

server = socket.socket(type=socket.SOCK_DGRAM)
server.bind(ADDRESS)
server.setblocking(False)

conn = socket.socket(type=socket.SOCK_DGRAM)
conn.setblocking(False)
office = orudp.Office(conn)
sent = office.send_message(message, 1, 1, ADDRESS)
print("sent {} bytes".format(sent)) 

def read(socket):
    data, host = socket.recvfrom(1024)
    print("read", data)
    socket.sendto(b"Ok", host)

selector = selectors.DefaultSelector()
selector.register(server, selectors.EVENT_READ, read)

while True:
    office.run()
    if office.empty():
        break
    events = selector.select(0)
    for key, mask in events: 
        callback = key.data
        callback(key.fileobj)

print("bye")
