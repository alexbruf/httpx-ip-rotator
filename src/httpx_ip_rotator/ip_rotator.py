import httpx
from httpx_ip_rotator.rotator import DEFAULT_REGIONS, Rotator


class ApiGatewayTransport(httpx.HTTPTransport):
    """
    A transport that routes requests through AWS API Gateway.
    """
    def __init__(self, site, regions=DEFAULT_REGIONS, access_key_id=None, access_key_secret=None, verbose=True, **kwargs):
        super().__init__(**kwargs)
        # Set simple params from constructor
        self.rotator = Rotator(site, regions, access_key_id, access_key_secret, verbose)
    # Enter and exit blocks to allow "with" clause
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def start(self, force=False, require_manual_deletion=False, endpoints=[]):
        return self.rotator.start(force, require_manual_deletion, endpoints)

    def shutdown(self, endpoints=None):
        return self.rotator.shutdown(endpoints)
        

    def handle_request(self, request: httpx.Request):
        return super().handle_request(self.rotator._handle_request(request))

