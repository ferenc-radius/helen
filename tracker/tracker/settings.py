from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    workers: int = 1  # set default to 1, there is no need for more because we are running in a container.
    reload: bool = False
    version: str = "1.0.0"
    prune_node_interval: int = 5 * 60  # in seconds


@lru_cache()
def get_settings() -> Settings:
    return Settings()
