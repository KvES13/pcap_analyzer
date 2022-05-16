from scapy.all import *
from scapy.layers.http import * #HTTPRequest
from scapy.layers.dns import *
from scapy.layers.inet import UDP

from datetime import datetime
import sys

def getIPs(dataset):
    output = set()
    for i in dataset:
        output.add(i[1])
        output.add(i[2])
    return output

index = 0
for _ in sys.argv:
    if _=="--file":
        filename = sys.argv[index+1]
        print(f"filename={filename}")
    index += 1

#def sniff_callback(packet):
#    print(packet.payload.layers())  # display all layers
#    first_layer = packet[packet.payload.layers()[0]]  # access first layer of the list

start_time = datetime.now()
tmp = rdpcap(filename)
file_opening = "database opening time = " + str(datetime.now()-start_time)

start_time = datetime.now()
dataset = []
count = 0
for i in tmp:
    if HTTP in i or TCP in i or UDP in i:
        count += 1
        dataset.append([count, i["IP"].src, i["IP"].dst, i["Raw"] if Raw in i else "null"])

print(file_opening)
print(f"database processing time = {datetime.now() - start_time}")

print("result dataset")
for i in dataset:
    print(i[:-1])

print("IPs:", *getIPs(dataset))