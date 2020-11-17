"""Class BasicTunnel."""

import socket
import traceback
import threading

from tunnel.ITunnel import ITunnel
from config.tunnel.tunnel import MAX_CHUNK_SIZE


class BasicTunnel(ITunnel):
    """A basic tunnel, implements ITunnel interface."""

    def __init__(self, src_sock, dst_sock):
        """Initialize BasicTunnel source and destination sockets.

        Args:
            src_sock (Socket): Source socket for the tunnel objcect.
            dst_sock (Socket): Destination socket for the tunnel object.
        """
        self._src = src_sock
        self._dst = dst_sock

    def _tunnel_one_way(self, source, destination):
        """Read chunks of data from source and sends them to destination.

        Args:
            source (Socket): Input socket to read the chunks from.
            destination (Socket): Output socket to send the chunks to.
        """
        while True:
            try:
                data_read = source.recv(MAX_CHUNK_SIZE)
                if len(data_read) > 0:
                    destination.send(data_read)
                else:
                    break
            except Exception as e:
                print "Erorr on _tunnel_one_way: \r\n"
                traceback.print_exc()
                break

    def tunnel(self):
        """Tunnel between src_sock and dst_sock using two one way tunnels."""
        threading.Thread(target=self._tunnel_one_way,
                         args=(self._src, self._dst,)).start()
        threading.Thread(target=self._tunnel_one_way,
                         args=(self._dst, self._src,)).start()
