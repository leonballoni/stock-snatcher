import json
from contextlib import contextmanager
from loguru import logger
from seedwork.singleton import BaseSingleton
import redis


class NoOpRedisClient:
    """A no-op Redis client for fallback when Redis is not available."""

    def get(self, key: str):
        return None

    def setex(self, key: str, ttl: int, value: str):
        pass

    def ping(self):
        return False


class RedisServer(metaclass=BaseSingleton):
    """
    Singleton class that provides a connection to a Redis server and methods for
    interacting with the Redis database.
    """

    def __init__(self, url: str):
        self.url = url
        try:
            client_pool = redis.ConnectionPool.from_url(url)
            self.client = redis.StrictRedis(
                connection_pool=client_pool, decode_responses=True
            )
            if not self.client.ping():
                raise Exception("Failed initial ping")
            logger.info("REDIS Connected")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = NoOpRedisClient()

    @contextmanager
    def get_redis_client(self):
        client = redis.StrictRedis(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        try:
            yield client
        finally:
            client.close()

    def get_item(self, key: str) -> str | None:
        """
        Args:
            key (str): The key to retrieve the item from the client.

        Returns:
            str | None: The item retrieved from the client if found; otherwise, None.
        """
        item: str = self.client.get(key)
        if item:
            logger.debug("item encontrado")
            return item
        logger.debug("Nenhum item encontrado")
        return None

    def set_item(self, key: str, value: str, ttl: int = 300):
        try:
            self.client.setex(key, ttl, value)
            logger.debug(f"Item added to cache >>> {key}")
        except Exception as exp:
            logger.error(f"Erro em gerar cache {exp}")
            raise exp
