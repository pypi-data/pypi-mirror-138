

from nats.aio.client import Client as NATS

from libcatapult import asyncutils
from libcatapult.queues.base_queue import BaseQueue, NotConnectedException


class NatsQueue(BaseQueue):

    def __init__(self, server: str):
        """
        NatsQueue requires the server url to connect to.
        :param server: url of the server to connect to.
        """
        super().__init__()
        self.server = server
        self.connection = None

    def connect(self):
        if not self.connection:
            options = {
                "servers": [self.server],
            }
            self.connection = NATS()
            asyncutils.run(self.connection.connect(**options))
        return self.connection

    def close(self):
        if self.connection:
            asyncutils.run(self.connection.close())
            self.connection = None

    def publish(self, channel: str, message: str):
        if not self.connection:
            raise NotConnectedException()
        asyncutils.run(self.connection.publish(channel, message.encode("utf8")))

    # TODO: implement. ES: Don't need this currently so not implementing
    def receive(self, channel: str, timeout: int):
        raise NotImplemented

    def empty(self, channel: str):
        raise NotImplemented
