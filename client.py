from proxy.server_proxy import ServerProxy

def main():
    proxy = ServerProxy()
    proxy.start_proxy()

if __name__ == '__main__':
    main()