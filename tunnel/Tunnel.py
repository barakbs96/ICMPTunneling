import threading
import socket

from tunnel.ITunnel import ITunnel
from config.tunnel.network import MAX_SIZE


class Tunnel(ITunnel):
    def __init__(self, src_sock, dst_sock):
        self._src_sock = src_sock
        self._dst_sock = dst_sock

    def _one_way_tunnel(self, src, dst):
        while True:
            try:
                data = src.recv(MAX_SIZE)
                if len(data) > 0:
                    dst.send(data)
                else:
                    break
            except Exception as e:
                print str(e)
                break

    def start_tunneling(self):
        src_to_dst = threading.Thread(target=self._one_way_tunnel, args=(self._src_sock, self._dst_sock,))
        src_to_dst.start()
        dst_to_src = threading.Thread(target=self._one_way_tunnel, args=(self._dst_sock, self._src_sock,))
        dst_to_src.start()
