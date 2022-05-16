from scapy.all import *
from scapy.layers.http import *  # HTTPRequest

from scapy.layers.dns import *
from scapy.layers.inet import *
from scapy.layers.l2 import *

from .getGeoIP import *
from .cache import *
#from numpy.core import _

#from numba import jit

from .data_extract import *
from .mac import *

from datetime import datetime
import sys, glob, os

#@jit(nopython=True)
def get_protocol_info(pack):
    #sniff_callback(pack)
    if pack.haslayer(HTTP):
        return "HTTP"
    if pack.haslayer(TCP):
        return "TCP"
    # FIXME
    # if pack.haslayer(HTTPS):
    #    return "HTTPS"
    if pack.haslayer(UDP):
        return "UDP"
    if pack.haslayer(DNS):
        return "DNS"
    # FIXME
    # if pack.haslayer(FTP):
    #    return "FTP"
    # if pack.haslayer(Telnet):
    #    return "Telnet"
    # if pack.haslayer(SSH):
    #    return "SSH"

    if pack.haslayer(IP):
        return "IP"
    if pack.haslayer(ICMP):
        return "ICMP"

    if pack.haslayer(ARP):
        return "ARP"
    #FIXME
    if pack.haslayer(Ether):
        return "Ethernet"
    #else:
    return "NOT RECOGNIZED"

'''
web_patternu = re.compile(r'((txtUid|username|user|name)=(.*?))&', re.I)
web_patternp = re.compile(r'((txtPwd|password|pwd|passwd)=(.*?))&', re.I)
tomcat_pattern = re.compile(r'Authorization: Basic(.*)')
'''
#@jit(nopython=True)
def get_dangerous_info(tcp_dict, http_dict, pack, PCAPS):
    if HTTP in pack:
        '''global web_patternu
        global web_patternp
        global tomcat_pattern
        '''
        try:
            data = str(bytes(pack["Raw"].load).decode("utf8", "replace"))
        except:
            return "undefined"
        # HTTP
        for pattn, attk in http_dict.items():
            if pattn.upper() in data.upper():
                return attk
        ''' 
        host_ip = pack["IP"].src
        webdata = web_data(PCAPS, host_ip)
        webbur_list = list()

        for web in webdata:
            data = web['data']
            # HTTP
            username = web_patternu.findall(data)
            password = web_patternp.findall(data)
            tomcat = tomcat_pattern.findall(data)
            if username or password or tomcat:
                webbur_list.append(web['ip_port'].split(':')[0])
            for pattn, attk in http_dict.items():
                if pattn.upper() in data.upper():
                    return attk
            '''
    elif TCP in pack:
        sport = pack["TCP"].sport
        dport = pack["TCP"].dport
        if sport in tcp_dict:
            return tcp_dict[sport]
        elif dport in tcp_dict:
            return tcp_dict[dport]

    #FIXME FTP, SSH

    return "no malware"


@lfu_cache
def get_geo_cached(address):
    return get_geo(address)

#@jit(nopython=True)
def get_pack_raw(pack):
    methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']  # http methods
    if Raw in pack:
        # print(f'RAW={hexdump(pack["Raw"])}')
        for m in methods:
            str1 = str(linehexdump(pack["Raw"].load, dump=True, onlyasc=True))
            if m in str1:
                return str(bytes(pack["Raw"].load).decode("utf8", "replace"))
        
        return str(linehexdump(pack["Raw"].load, dump=True, onlyasc=True))
    else:
        return "no info found"

    return "you shouldn't see this"


def sniff_callback(packet):
    print(packet.payload.layers())  # display all layers

#@jit(nopython=True)
def get_host_ip(PCAPS):
    ip_list = list()
    for pcap in PCAPS:
        if pcap.haslayer(IP):
            ip_list.append(pcap.getlayer(IP).src)
    return ip_list


#@jit(nopython=True)
def getDataset(count=0):
    '''
    index = 0
    for _ in sys.argv:
        if _=="--file":
            filename = sys.argv[index+1]
            print(f"filename={filename}")
        index += 1
    '''

    if os.name == "posix":
        list_of_files = glob.glob("static/UploadedFiles/*")
    else:
        list_of_files = glob.glob("static\\UploadedFiles\\*")

    #print(list_of_files)
    filename = max(list_of_files, key=os.path.getctime)
    print(filename)
    mac_reader = MACAddressReader()
    #splited_path = filename.split("/")
    #for _ in splited_path:
    #    print('Test ', _)
    #filename = "\\".join(splited_path)
        #filename = "main/workFiles/mix.cap"
    #print(filename)

    start_time = datetime.now()
    tmp = rdpcap(filename)
    #print("Readed pcap")
    file_opening = "database opening time = " + str(datetime.now() - start_time)

    start_time = datetime.now()
    dataset = []

    with open('main/utils/protocol/WARN', 'r', encoding='UTF-8') as f:
        warns = f.readlines()
    TCP_DICT = dict()
    for warn in warns:
        warn = warn.strip()
        TCP_DICT[int(warn.split(':')[0])] = warn.split(':')[1]

    with open('main/utils/warning/HTTP_ATTACK', 'r', encoding='UTF-8') as f:
        attacks = f.readlines()
    WEB_DICT = dict()
    for attack in attacks:
        attack = attack.strip()
        WEB_DICT[attack.split(' : ')[0]] = attack.split(' : ')[1]

    print(len(tmp))
    for i in tmp:
        pct_info = {}
        pct_info["protocol"] = get_protocol_info(i)
        pct_info["id_pack"] = count
        count += 1

        pct_info["time"] = str(datetime.now() - start_time)
        #IP
        if IP in i:
            pct_info["source_ip"] = i["IP"].src
            pct_info["destination_ip"] = i["IP"].dst
        elif ARP in i:
            pct_info["source_ip"] = i["ARP"].psrc
            pct_info["destination_ip"] = i["ARP"].pdst
        else: #pure Ethernet
            pct_info["source_ip"] = "no info"
            pct_info["destination_ip"] = "no info"

        raw_data = get_pack_raw(i)
        pct_info["packet_length"] = len(raw_data)
        pct_info["info"] = raw_data

        pct_info["extinfo"] = get_dangerous_info(TCP_DICT, WEB_DICT, i, tmp)

        if TCP in i:
            pct_info["src_port"] = i["TCP"].sport
            pct_info["dst_port"] = i["TCP"].dport
        elif UDP in i:
            pct_info["src_port"] = i["UDP"].sport
            pct_info["dst_port"] = i["UDP"].dport
        else:
            pct_info["src_port"] = "unknown port"
            pct_info["dst_port"] = "unknown port"

        pct_info["src_mac"] = i["Ethernet"].src
        pct_info["src_vendor"] = mac_reader.get_vendor_by_mac(pct_info["src_mac"])
        pct_info["dst_mac"] = i["Ethernet"].dst
        pct_info["dst_vendor"] = mac_reader.get_vendor_by_mac(pct_info["dst_mac"])

        if ARP in i:
            pct_info["ip_type"] = i["ARP"].ptype
        elif IP in i:
            pct_info["ip_type"] = "IPv" + str(i["IP"].version)
        else:
            pct_info["ip_type"] = "no info"

        if ARP in i:
            pct_info["ttl"] = -1
        elif IP in i:
            pct_info["ttl"] = i["IP"].ttl
        else:
            pct_info["ttl"] = -1


        ipInfo1 = get_geo_cached(pct_info["source_ip"])
        ipInfo2 = get_geo_cached(pct_info["destination_ip"])
        pct_info["country1"] = ipInfo1["country"]
        pct_info["country2"] = ipInfo2["country"]
        pct_info["city1"] = ipInfo1["city"]
        pct_info["city2"] = ipInfo2["city"]
        pct_info["long1"] = ipInfo1["long"]
        pct_info["lat1"] = ipInfo1["lat"]
        pct_info["long2"] = ipInfo2["long"]
        pct_info["lat2"] = ipInfo2["lat"]

        #print("zapisali paket - ", count)
        dataset.append(pct_info)

    #print(file_opening)
    print(f"database processing time = {datetime.now() - start_time}")
    return dataset


if __name__ == '__main__':
    getDataset()