#!/usr/bin/python3


class MACAddressReader():
    '''Use with files which contains information like this:\n
    ...\n
    000003	XEROX CORPORATION\n
    ...'''
    def __init__(self, file_name='main/mac-vendor.txt'):
        self.mac_to_vendor = dict()
        with open(file_name) as f:
            for line in f.readlines():
                mac, vendor = line[0:6], line[7:].strip()
                self.mac_to_vendor[mac] = vendor
    

    def get_mac_vendor_part(mac):
        '''40:b0:76:41:85:f6 -> 40B076\n
        or\n
        40b0764185f6 -> 40B076'''
        mac = mac.strip().upper()
        if mac[2] == mac[5] == mac[8] == mac[11] == mac[14] == ':':
            tokens = mac.upper().split(":")
            return tokens[0] + tokens[1] + tokens[2]
        elif len(mac) == 12:
            return mac[0:6]
        else:
            #raise Exception('Wrong MAC-address')
            return 'Wrong MAC-address: ' + mac

    def get_vendor_by_mac(self, mac):
        '''00:00:03:41:85:f6 -> XEROX CORPORATION'''
        try:
            return self.mac_to_vendor[MACAddressReader.get_mac_vendor_part(mac)]
        except KeyError:
            return 'Unknown vendor'


if __name__ == '__main__':
    # Tests
    #myMAC = '40:b0:76:41:85:f6'
    myMAC = '00:0c:6d:41:85:f6'
    #myMAC = '000c6d4185f6'
    #myMAC = '00:0c:6d:41:85f6'
    #myMAC = '000c6d41856'

    mar = MACAddressReader()
    vendor = mar.get_vendor_by_mac(myMAC)
    print(vendor)

