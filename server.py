"""Server Main."""
from proxy.icmp_ht_proxy import ICMPHTProxy
from proxy.ht_proxy import HTProxy


def main():
    """Start serving clients as icmp http proxy."""
    ICMPHTProxy().start_proxy()


if __name__ == '__main__':
    main()
