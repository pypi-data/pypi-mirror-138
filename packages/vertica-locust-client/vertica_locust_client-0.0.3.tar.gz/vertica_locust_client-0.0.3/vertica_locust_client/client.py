
import logging
import time
import vertica_python
from carbon.client.extras import SimpleTimer
from carbon.client import UDPClient


class VerticaClient():
    def __init__(self, host, environment):
        self._request_event = environment.events.request
        self.host = host
        self.conn_info = {
            'host': host,
            'port': 5433,
            'user': environment.parsed_options.user,
            'password': environment.parsed_options.password,
            'connection_timeout': 10
        }
        logging.info(self.conn_info)
        if environment.parsed_options.carbon_endpoint != "":
            self.carbon_client = UDPClient(environment.parsed_options.carbon_endpoint,
                                           environment.parsed_options.carbon_namespace)
        else:
            self.carbon_client = None

    def make_cursor(self, carbon_metric="cursor"):
        """Establish a connection to Vertica and construct a cursor object"""
        return VerticaCursor(self.conn_info, self._request_event, self.carbon_client, carbon_metric)


class VerticaCursor():
    def __init__(self, conn_info, request_event, carbon_client, carbon_metric):
        self.conn = vertica_python.connect(**conn_info)
        self.cursor = self.conn.cursor()
        self._request_event = request_event
        self.carbon_client = carbon_client
        self.carbon_metric = carbon_metric

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.conn.close()

    def __getattr__(self, name):
        attr = self.cursor.__getattribute__(name)

        def wrapper(*args, **kwargs):
            if not callable(attr):
                return attr

            # Only the calls to execute() will be logged through locust
            if name != 'execute':
                return attr(*args, **kwargs)

            request_meta = {
                "request_type": "vertica",
                "name": "execute",
                "start_time": time.time(),
                "response_length": 0,
                "response": None,
                "context": {},
                "exception": None,
            }
            start_perf_counter = time.perf_counter()
            try:
                if self.carbon_client:
                    with SimpleTimer(self.carbon_metric, self.carbon_client):
                        r = attr(*args, **kwargs)
                else:
                    r = attr(*args, **kwargs)
                request_meta["response"] = r
            except Exception as e:
                request_meta["exception"] = e
            request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
            self._request_event.fire(**request_meta)
            if self.carbon_client:
                self.carbon_client.send()
            return request_meta["response"]

        return wrapper