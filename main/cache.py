#import ip


def lfu_cache(func_to_decorate, maxsize=128, cache_latency=0):
    '''Cache with "Least Frequently Used" strategy'''
    frequency = {}
    cache = {}

    def new_func(argument):
        if argument not in frequency:
            frequency[argument] = 1
        else:
            frequency[argument] += 1
            
        if argument not in cache and len(cache) >= maxsize:
            min_value = min(map(lambda key: frequency[key], cache))
            if frequency[argument] > min_value + cache_latency:
                for key in frequency:
                    if frequency[key] == min_value and key in cache:
                        min_key = key
                cache.pop(min_key)
                cache[argument] = func_to_decorate(argument)
            else:
                return func_to_decorate(argument)
        elif argument not in cache and len(cache) < maxsize:
            cache[argument] = func_to_decorate(argument)

        return cache[argument]

    return new_func


'''
@lfu_cache
def ip2(address):
    return ip.IPInfo.getInfoAboutIP(address)

@lfu_cache
def f(s):
    sum = 0
    for number in s:
        sum *= int(number)#

    return sum

'''

if __name__ == '__main__':
    '''
    ss = ['1111111111111111111111111111111111111111111111111111999999999999999999999' for x in range(1000000)]
    print(len(ss))
    for s in ss:
        f(s)
    '''
    p = '83.239.95.114'

    for i in range(1000):
        print('i = ' + str(i))
        #print(ip.IPInfo.getInfoAboutIP(p))
        #print(ip2(p))
        
        print() 



