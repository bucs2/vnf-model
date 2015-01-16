import socket

SWITCH_H2_IP = '10.0.3.2'
H2_PORT = 5002
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((SWITCH_H2_IP, H2_PORT))

count = 0
while 1:
    data, addr = s.recvfrom(BUFFER_SIZE)
    if not data: break
    if data.decode('UTF-8') == '0':
        break
    count += 1
print("Received", count, "packets.")


