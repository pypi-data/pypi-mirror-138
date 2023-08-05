from abc import abstractmethod


class NotConnectedException(Exception):
    pass


class BaseQueue(object):
    """
    BaseQueue allows for the swapping of queue technologies under the hood.

    Once created you should need to call connect() to actually establish a connection.
    When you are done you should call close()
    """
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Establish a connection to the actual service that we are wanting
        :return: nothing
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the underlying connection
        :return: nothing
        """
        pass

    @abstractmethod
    def publish(self, channel: str, message: str):
        """
        Send a message to the underlying connection.

        Will throw a NotConnectedException if connect has not been called.
        :param channel:
        :param message:
        :return:
        """
        pass

    @abstractmethod
    def receive(self, channel: str, timeout: int):
        """
        receive a message from the queue.

        Will throw a NotConnectedException if connect has not been called.

        :param channel: the channel to receive from
        :param timeout: how long to wait if nothing is available to receive.
        :return: the message received
        """
        pass

    @abstractmethod
    def empty(self, channel: str):
        """
        will return True if the channel is empty
        :param channel: the channel to check for being empty
        :return: True or False
        """
        pass
