from contextlib import AbstractContextManager
from typing import Any, Callable, Optional
from ..core_db import DbSession


class CacheRepository:
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        super().__init__()

        with db_session_factory() as db_session:
            self.cache_db_client = db_session.cache_db_client

    def set(
        self,
        key: str,
        value: str,
        context: Optional[Any] = None,
    ):
        try:
            self.cache_db_client.set(key, value)
            return True
        except:
            return False

    def get(
        self,
        key: str,
        context: Optional[Any] = None,
    ):
        try:
            data = self.cache_db_client.get(key)
            return data
        except:
            return False

    def fetch_list_of_dicts(
        self,
        key: str,
        context: Optional[Any] = None,
    ):
        try:
            hash_keys = self.cache_db_client.keys(f"{key}:*")

            # Fetch the dictionaries from Redis
            list_of_dicts = [
                self.cache_db_client.hgetall(hash_key) for hash_key in hash_keys
            ]

            return list_of_dicts

        except:
            return False

    def set_list_of_dicts_in_redis(self, key: str, list_of_dicts: list):
        try:
            for index, dictionary in enumerate(list_of_dicts):
                hash_key = f"{key}:{index}"

                self.cache_db_client.hmset(hash_key, dictionary)

            return True

        except:
            return False
