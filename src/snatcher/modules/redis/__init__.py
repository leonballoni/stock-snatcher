import json
from contextlib import contextmanager
from loguru import logger
from seedwork.singleton import BaseSingleton
import redis

class RedisServer(metaclass=BaseSingleton):
    def __init__(self, host: str, password: str, port: int, db: str):
        self.host = host
        self.password = password
        self.port = port
        self.database = db
        client_pool = redis.ConnectionPool(host=self.host,
                                            port=self.port,
                                            db=self.database)
        self.client = redis.StrictRedis(connection_pool=client_pool,
                                        decode_responses=True)

    @contextmanager
    def get_redis_client(self):
        client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        try:
            yield client
        finally:
            client.close()

    def get_item(self, key: str) -> str | None:
        item: str = self.client.get(key)
        if item:
            logger.debug("item encontrado")
            return item
        logger.debug("Nenhum item encontrado")
        return None


    def set_item(self, key: str, value, ttl: int = 300):
        try:
            self.client.setex(key, ttl, json.dumps(value))
            logger.debug(f"Item added to cache >>> {key}")
        except Exception as exp:
            logger.error(f"Erro em gerar cache {exp}")
            raise exp
