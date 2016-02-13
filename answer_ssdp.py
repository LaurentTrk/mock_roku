import socket
import struct
import random
from time import time, sleep

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900

multicast_group_c = SSDP_ADDR
server_address = ('', SSDP_PORT)

ROKU_ADDR = "192.168.2.15"
ROKU_PORT = 8060
ROKU_USN  = "uuid:roku:ecp:P0A070000009"

M_SEARCH_MSG   = 'M-SEARCH * HTTP/1.1'
M_RESPONSE_MSG = 'HTTP/1.1 200 OK\r\nCACHE-CONTROL: max-age = 2 \r\nLocation: http://%s:%d/\r\nST: roku:ecp\r\nUSN: %s\r\n' % (ROKU_ADDR, ROKU_PORT, ROKU_USN)

def answer_ssdp():
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    # add the socket to the multicast group on all interfaces.
    group = socket.inet_aton(multicast_group_c)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print('\n waiting to receive')
        datab, address = sock.recvfrom(1024)    
        print('received %s bytes from %s' % (len(datab), address))
        print(datab)
        data = datab.decode("utf-8") 
        #discard message if header is not in right format 
        if data[0:19]== M_SEARCH_MSG:
            if data.find("ST: ssdp:all") != -1 : 
                mxpos = data.find("MX:")     
                maxdelay = int(data[mxpos+4]) % 5   #Max value of this field is 5			
                sleep(random.randrange(0, maxdelay+1, 1))  #wait for random 0-MX time until sending out responses using unicast.
                sock.sendto(M_RESPONSE_MSG.encode('utf-8'), address)
            else:
                print('MSearch with ST field != ssdp:all')
        else:
            print('received wrong MSearch')

answer_ssdp()           