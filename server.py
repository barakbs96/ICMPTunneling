from proxy.ICMPHTTPProxy import ICMPHTTPProxy
from proxy.HTTPProxy import HTTPProxy

def main():
    proxy = ICMPHTTPProxy()
    proxy.serve()

if __name__ == '__main__':
    main()