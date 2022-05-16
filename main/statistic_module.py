from .models import packet

def get_http_requests_stats(_method):
    all_http_packs = packet.objects.filter(protocol='HTTP')    
    good_http_packs = all_http_packs.exclude(info='unknown RAW data')
    for i in good_http_packs.filter(info__contains=_method):
        #print(i.info)
        #print(i)
        return ("")
    return good_http_packs.get(info__contains=_method)

def get_proto_stats(_protocol):
    all_packets = packet.objects.filter(protocol=_protocol)
    return len(all_packets)

if __name__ == '__main__':
    print(get_proto_stats("tcp"))


