class ITunnel(object):
    def __init__(self, src_sock, dst_sock):
        raise NotImplementedError

    def start_tunneling(self):
        raise NotImplementedError