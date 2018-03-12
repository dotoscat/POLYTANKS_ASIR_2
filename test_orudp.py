import unittest

import time
import signal
import orudp

signal.signal(signal.SIGINT, signal.SIG_DFL)

ADDRESS = ('127.0.0.1', 1337)

message = b'Hola mundo'

def read_message(message, address, mailbox):
    print("read from read", message, address)
    mailbox.send_message(b'Ok', 1, address=address)
    mailbox.send_message(b'Un besillo', 0.5, address=address)

server_office = orudp.Mailbox(bind=ADDRESS, protocol=read_message)

conn_office = orudp.Mailbox()
sent = conn_office.send_message(message, 1, tries=1, address=ADDRESS)
print("sent {} bytes".format(sent)) 

while True:
    conn_office.run()
    server_office.run()
    if conn_office.empty():
        #break
        pass
    time.sleep(0.01)

print("bye")
