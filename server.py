from proxy.icmp_ht_proxy import ICMPHTProxy
from proxy.ht_proxy import HTProxy

def main():
    proxy = ICMPHTProxy()
    proxy.start_proxy()

if __name__ == '__main__':
    main()