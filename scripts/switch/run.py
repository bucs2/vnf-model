import socket
import _thread

H1_SWITCH_IP = '10.0.1.1'

SWITCH_IDS1_IP = '10.0.5.3'
SWITCH_IDS2_IP = '10.0.6.2'

IDS1_SWITCH_IP = '10.0.5.1'
IDS_SWITCH_PORT = 5010

IDS1_H2_PORT = 5004
IDS1_H3_PORT = 5005
IDS2_H3_PORT = 5006

SWITCH_H2_IP = '10.0.3.2'
H2_PORT = 5002
SWITCH_H3_IP = '10.0.4.2'
H3_PORT = 5003

BUFFER_SIZE = 20

sent = 0
ssids1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ssids2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ids = ssids1
ids_ip = SWITCH_IDS1_IP
ids_port = IDS1_H3_PORT

def flow_to_h2():
    # Incoming flow from H1.
    s1s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1s.bind((H1_SWITCH_IP, H2_PORT))

    # Outgoing flows to H2 and IDS1.
    ss2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssi1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    count = 0
    ids = ssi1
    ids_ip = SWITCH_IDS1_IP
    ids_port = IDS1_H2_PORT
    while 1:
        data, addr = s1s.recvfrom(BUFFER_SIZE)
        if not data: break
        ss2.sendto(data, (SWITCH_H2_IP, H2_PORT))  # Forward to H2.
        ids.sendto(data, (ids_ip, ids_port))       # Forward to IDS.
        if data.decode('UTF-8') == '0':
            break
        count += 1

    print("Forwarded", count, "packets to H2.")

def flow_to_h3():

    global sent
    global ids
    global ids_ip
    global ids_port

    s1s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1s.bind((H1_SWITCH_IP, H3_PORT))

    ss3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    count = 0
    while 1:
        data, addr = s1s.recvfrom(BUFFER_SIZE)
        if not data: break
        ss3.sendto(data, (SWITCH_H3_IP, H3_PORT))  # Forward to H3.
        ids.sendto(data, (ids_ip, ids_port))       # Forward to IDS.
        if data.decode('UTF-8') == '0':
            break
        count += 1
        sent += 1

    print("Forwarded", count, "packets to H3.")

def check_sla():

    global sent
    global ids
    global ids_ip
    global ids_port

    sids1s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sids1s.bind((IDS1_SWITCH_IP, IDS_SWITCH_PORT))

    while 1:
        try:
            data, addr = sids1s.recvfrom(BUFFER_SIZE)
            data = data.decode('UTF-8')
            rcvd = int(data)
            print(str(rcvd / sent))
            if rcvd / sent < .95 and ids == ssids1:
                # Perform migration to IDS2.
                print("Migrating to IDS2")
                ids = ssids2
                ids_ip = SWITCH_IDS2_IP
                ids_port = IDS2_H3_PORT
                sent = 100
            elif rcvd / sent < .75 and ids == ssids2:
                print("Migrating to IDS1")
                # Migrate back to IDS1.
                ids = ssids1
                ids_ip = SWITCH_IDS1_IP
                ids_port = IDS1_H3_PORT
        except:
            pass

try:
   _thread.start_new_thread(flow_to_h2, ())
   _thread.start_new_thread(flow_to_h3, ())
   _thread.start_new_thread(check_sla, ())
except:
   print("Error: unable to start thread")

while 1:
    pass

