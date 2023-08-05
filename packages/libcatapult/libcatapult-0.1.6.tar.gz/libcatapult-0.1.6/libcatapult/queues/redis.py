import redis as redis

from libcatapult.queues.base_queue import BaseQueue, NotConnectedException


class RedisQueue(BaseQueue):
    """
    RedisQueue is an implementation of BaseQueue for talking to redis queues.
    """

    def __init__(self, host: str, port: str):
        """
        RedisQueue requires the host and port parameters
        :param host: host name of the redis servers
        :param port: port number ot connect to.
        """
        super().__init__()
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = redis.Redis(host=self.host, port=self.port, db=0)

        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def publish(self, channel: str, message: str):
        if not self.connection:
            raise NotConnectedException()
        self.connection.rpush(channel, message)

    def receive(self, channel: str, timeout: int = 1):
        if not self.connection:
            raise NotConnectedException()
        item = self.connection.brpop(channel, timeout=timeout)[1]
        return item.decode("utf-8")

    def empty(self, channel: str):
        if not self.connection:
            raise NotConnectedException()
        print(self.connection.llen(channel))
        return self.connection.llen(channel) == 0
