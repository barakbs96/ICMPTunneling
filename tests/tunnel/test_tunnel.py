import pytest
import socket
import threading
from tunnel.basic_tunnel import BasicTunnel

# def test_bla():
#     print 'bla'
#     assert 1 == 1


def test_tunnel_both_ways():
    print 'bla'
    server_socket = socket.socket()
    ip = '127.0.0.1'
    port = 7859
    server_socket.bind((ip, port))
    server_socket.listen(2)

    client1_to_server = socket.socket()
    client1_to_server.connect((ip, port))
    server_to_client1 = server_socket.accept()[0]

    client2_to_server = socket.socket()
    client2_to_server.connect((ip, port))
    server_to_client2 = server_socket.accept()[0]

    basic_tunnel = BasicTunnel(server_to_client1, server_to_client2)
    basic_tunnel.tunnel()
    data_sent_client1 = 'get this'
    client1_to_server.send(data_sent_client1)
    data_received_client2 = client2_to_server.recv(30)

    data_sent_client2 = 'get this2'
    client2_to_server.send(data_sent_client2)
    data_received_client1 = client1_to_server.recv(30)

    assert (data_sent_client1 == data_received_client2 and
            data_sent_client2 == data_received_client1)
