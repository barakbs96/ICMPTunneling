"""Client Main."""
from proxy.server_proxy import ServerProxy


def main():
    """Start tunnel browser data to server."""
    ServerProxy().start_proxy()


if __name__ == '__main__':
    main()
