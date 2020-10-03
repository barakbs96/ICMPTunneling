class ISocket(object):
    def bind(self):
        raise NotImplementedError

    def accept(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def send(self, data):
        raise NotImplementedError

    def recv(self, amount):
        raise NotImplementedError