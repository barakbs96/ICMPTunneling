from proxy.ICMPHTTPProxy import ICMPHTTPProxy
from proxy.ht_proxy import HTProxy

def main():
    proxy = ICMPHTTPProxy()
    proxy.start_proxy()

if __name__ == '__main__':
    main()