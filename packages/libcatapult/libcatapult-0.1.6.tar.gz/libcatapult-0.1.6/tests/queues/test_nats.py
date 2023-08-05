from mock import AsyncMock
from nats.aio.client import Client as NATS
import pytest

from libcatapult.queues.base_queue import NotConnectedException
from libcatapult.queues.nats import NatsQueue


def test_not_connected():
    nc = NatsQueue("nats://somewhere:12345")
    with pytest.raises(NotConnectedException):
        nc.publish("a channel", "a message")


def test_nats_double_disconnect():
    nc = NatsQueue("nats://somewhere:12345")
    nc.connection = NATS()
    nc.connection.connect = AsyncMock()
    mock_close = AsyncMock()
    nc.connection.close = mock_close

    nc.close()
    nc.close()

    mock_close.assert_called_once()


def test_nats_send():
    nc = NatsQueue("nats://somewhere:12345")
    nc.connection = NATS()
    nc.connection.connect = AsyncMock()
    nc.connection.close = AsyncMock()
    nc.connection.publish = AsyncMock()
    nc.publish("a channel", "a message")

    nc.connection.publish.assert_called_once_with("a channel", "a message".encode("utf8"))
