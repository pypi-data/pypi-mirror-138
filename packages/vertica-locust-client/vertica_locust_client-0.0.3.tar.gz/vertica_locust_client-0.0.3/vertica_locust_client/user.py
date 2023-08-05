from os import environ
from locust import User
from vertica_locust_client import VerticaClient


class VerticaUser(User):
    abstract = True
    def __init__(self, environment):
        super().__init__(environment)
        self.client = VerticaClient(self.host, environment)
