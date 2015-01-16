import socket
import _thread

SWITCH_IDS1_IP = '10.0.5.3'
IDS1_SWITCH_IP = '10.0.5.1'
IDS1_H2_PORT = 5004
IDS1_H3_PORT = 5005
IDS_SWITCH_PORT = 5010

BUFFER_SIZE = 20

def flow_of_h2():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SWITCH_IDS1_IP, IDS1_H2_PORT))

    count = 0
    while 1:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if not data: break
        if data.decode('UTF-8') == '0':
            break
        count += 1
    print("Received", count, "packets for H2.")

def flow_of_h3():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SWITCH_IDS1_IP, IDS1_H3_PORT))

    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    count = 0
    while 1:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if not data: break
        if data.decode('UTF-8') == '0':
            break
        count += 1
        #if count % 100 == 0:
        #    s2.sendto(str(count).encode('UTF-8'), (IDS1_SWITCH_IP, IDS_SWITCH_P
ORT))
    print("Received", count, "packets for H3.")

try:
   _thread.start_new_thread(flow_of_h2, ())
   _thread.start_new_thread(flow_of_h3, ())
except:
   print("Error: unable to start thread")

while 1:
    pass

