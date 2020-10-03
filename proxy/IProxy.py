class IProxy(object):
    def _setup_server_socket(self):
        raise NotImplementedError
    def serve(self):
        raise NotImplementedError
