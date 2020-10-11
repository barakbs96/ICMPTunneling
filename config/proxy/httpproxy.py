"""
HTTP Proxy Consts.

Attributes:
    CONNECT_HTTP_METHOD (str): HTTP connect string method.
    HOST_HTTP_HEADER (str): HTTP host header string.
    HTTP_PROXY_IP (str): IP address of HTTP proxy.
    HTTP_PROXY_PORT (int): Port the HTTP proxy listen on.
    MAX_CLIENTS_HTTP_PROXY (int): Max clients HTTP proxy will serve.
    MAX_DATA_SIZE (int): Max of data size.
    PROXY_CONNECT_HTTP_MESSEGE (str): HTTP connect message string.

"""
HTTP_PROXY_IP = '10.0.0.11'
HTTP_PROXY_PORT = 12345

MAX_CLIENTS_HTTP_PROXY = 10

MAX_DATA_SIZE = 65535

CONNECT_HTTP_METHOD = 'CONNECT'
HOST_HTTP_HEADER = 'host'
PROXY_CONNECT_HTTP_MESSEGE = 'HTTP/1.1 200 Connection Established\r\n\r\n'
