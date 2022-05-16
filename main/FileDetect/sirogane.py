from scapy.all import *
from collections import OrderedDict
import base64
import os
import re
import binascii


def all_files(pcap_file,stat, filePCAPname):

    PCAPS = rdpcap(pcap_file)
    print(1)
    folder = stat + 'detectFiles/'
    file_header = dict()
    with open(stat+ 'forFileDetect/FILES', 'r', encoding='UTF-8') as f:
        lines = f.readlines()
      

    """
    !!!
    Добавить приведение в нижний регистр
    """
    listOFnAMEFILES= []
    fileName = []
    print(2)
    for line in lines:
        file_header[line.split(':')[0].strip()] = line.split(':')[1].strip()
    sessions = PCAPS.sessions()
    # print(sessions['TCP 10.0.2.15:38090 > 10.13.16.21:5000'])
    allfiles_dict = OrderedDict()
    allpayloads_dict = OrderedDict()
    for sess, ps in sessions.items():
        payload = b''
        for p in ps:
            if p.haslayer(Raw):
                payload += p[Raw].load
            if payload:
                allpayloads_dict[sess] = payload
    i = 0
    for sess, payload in allpayloads_dict.items():
        datas = payload.split(b'\r\n\r\n')
        for data in datas:
            d = binascii.hexlify(data.strip())
            for header, suffix in file_header.items():
                if d.startswith(header.encode('UTF-8')):
                    filename = str(i) + suffix
                    print(folder+filename)
                    if not os.path.exists(folder+filePCAPname):
                        os.mkdir(folder+filePCAPname+'/')
                    with open(folder +filePCAPname+'/' + filename, 'wb') as f:
                        
                        f.write(binascii.unhexlify(d))
                    allfiles_dict[filename] = sess
                    listOFnAMEFILES.append(folder +filePCAPname+'/' + filename)
                    fileName.append(filename)
                    i += 1
    print(3)
    return listOFnAMEFILES,fileName

 
#all_files(PCAPS, 'tests')