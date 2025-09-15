from typing import Optional, Type
from .client import DatabaseClient


class DatabaseSingleton:
    _instance: Optional["DatabaseSingleton"] = None
    _client: Optional[DatabaseClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self, client_class: Type[DatabaseClient], *args, **kwargs) -> None:
        if self._client is None:
            self._client = client_class(*args, **kwargs)

    def get_client(self) -> DatabaseClient:
        if self._client is None:
            raise RuntimeError(
                "Database client not initialized. Call `initialize()` for singleton first."
            )

        return self._client


db_singleton = DatabaseSingleton()
