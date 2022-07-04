#!/usr/bin/python3

import socket
import sys
from time import sleep

def scanTCP(network, lowestPort, highestPort):
    results = []
    counter = 0
    for port in range(lowestPort, highestPort + 1):
        print(f"[SCANNING] {str(f'{port} / {highestPort}').ljust(20)}OPEN PORTS FOUND: {counter}", end="\r")
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = socket.create_connection((network, port))
            tcp.close()
            if result: #not tcp.connect_ex((network, port)):
                tcp.close()
                results.append(port)
                counter += 1
        except:
            tcp.close()
            pass
    output(network, results)
        
def output(network, results):
    if len(results) > 0:
        print("PORT    SERVICE" + "\t"*10)
        for index in range (len(results)):
            try:
                print(f"{str(results[index]).ljust(8)}{socket.getservbyport(results[index])}")
            except:
                print(f"{str(results[index]).ljust(8)}unknown")
                pass
    else:
        print("NO OPEN PORTS FOUND" + "\t"*10)

if __name__ == '__main__':
    socket.setdefaulttimeout(0.01)
    if len(sys.argv) >= 4:
        network = sys.argv[1]
        lowestPort = int(sys.argv[2])
        highestPort = int(sys.argv[3])
        scanTCP(network, lowestPort, highestPort)
    else:
        print("invalid syntax")