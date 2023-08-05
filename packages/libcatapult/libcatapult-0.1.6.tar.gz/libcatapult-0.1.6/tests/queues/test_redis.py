import fakeredis as fakeredis
import pytest

from libcatapult.queues.base_queue import NotConnectedException
from libcatapult.queues.redis import RedisQueue


def test_not_connected():
    redis = RedisQueue("somewhere", "12345")
    with pytest.raises(NotConnectedException):
        redis.publish("a channel", "a message")


def test_double_close():
    redis = RedisQueue("somewhere", "12345")
    redis.connection = fakeredis.FakeStrictRedis()

    redis.close()
    redis.close()


def test_normal():
    redis = RedisQueue("somewhere", "12345")
    redis.connection = fakeredis.FakeStrictRedis()
    redis.connect()  # shouldn't do anything as we have already set the connection to the fakeredis

    redis.publish("test", "wibble")

    assert redis.connection.lpop("test") == b'wibble'

    redis.close()


def test_receive():
    redis = RedisQueue("somewhere", "12345")
    redis.connection = fakeredis.FakeStrictRedis()
    redis.connect()  # shouldn't do anything as we have already set the connection to the fakeredis
    redis.publish("test", "wibble")
    result = redis.receive("test")
    assert result == "wibble"

def test_empty():
    redis = RedisQueue("somewhere", "12345")
    redis.connection = fakeredis.FakeStrictRedis()
    redis.connect()  # shouldn't do anything as we have already set the connection to the fakeredis

    assert redis.empty("test")
