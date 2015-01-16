import socket
import random
import time
import _thread

H1_SWITCH_IP = '10.0.1.1'
H2_PORT = 5002
H3_PORT = 5003
BUFFER_SIZE = 1024
MESSAGE = b"Hello, World!"

NUM_PACKETS = 40000

def send_to_h2():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(NUM_PACKETS):
        s.sendto(MESSAGE, (H1_SWITCH_IP, H2_PORT))
        time.sleep(.00001)

    time.sleep(5)
    s.sendto(b"0", (H1_SWITCH_IP, H2_PORT))
    s.close()

def send_to_h3():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(NUM_PACKETS):
        s.sendto(MESSAGE, (H1_SWITCH_IP, H3_PORT))
        time.sleep(.00001)

    time.sleep(5)
    s.sendto(b"0", (H1_SWITCH_IP, H3_PORT))
    s.close()

try:
   _thread.start_new_thread(send_to_h2, ())
   _thread.start_new_thread(send_to_h3, ())
except:
   print("Error: unable to start thread")

while 1:
    pass

