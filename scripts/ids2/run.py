import socket

SWITCH_IDS2_IP = '10.0.6.2'
IDS2_SWITCH_IP = '10.0.6.1'
IDS2_H3_PORT = 5006
IDS_SWITCH_PORT = 5010

BUFFER_SIZE = 20

def flow_of_h3():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SWITCH_IDS2_IP, IDS2_H3_PORT))

    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    count = 0
    while 1:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if not data: break
        if data.decode('UTF-8') == '0':
            break
        count += 1
        print("Receiving packets")
        if count % 100 == 0:
            s2.sendto(str(count).encode('UTF-8'), (IDS2_SWITCH_IP, IDS_SWITCH_PO
RT))
    print("Received", count, "packets for H3.")

flow_of_h3()

