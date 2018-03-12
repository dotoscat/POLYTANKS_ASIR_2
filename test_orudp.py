import unittest

import time
import signal
import orudp
import socket

signal.signal(signal.SIGINT, signal.SIG_DFL)

ADDRESS = ('127.0.0.1', 1337)

message = b'Hola mundo'

def read_message(message, address, mailbox):
    print("read from read", message, address)
    mailbox.send_message(b'Ok', 1, address=address)

server = socket.socket(type=socket.SOCK_DGRAM)
server.bind(ADDRESS)
server.setblocking(False)
server_office = orudp.Mailbox(server, read_message)

conn = socket.socket(type=socket.SOCK_DGRAM)
conn.setblocking(False)
conn_office = orudp.Mailbox(conn)
sent = conn_office.send_message(message, 1, tries=1, address=ADDRESS)
print("sent {} bytes".format(sent)) 

while True:
    conn_office.run()
    server_office.run()
    if conn_office.empty():
        #break
        pass

print("bye")
