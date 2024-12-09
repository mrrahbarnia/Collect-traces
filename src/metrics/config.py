from pydantic_settings import BaseSettings


class MetricConfig(BaseSettings):
    """
    Loading environment variables from .env
    """
    ADMIN_EMAIL: str
    MAX_MEMORY_PERCENT_ALERT: int
    MAX_CPU_PERCENT_ALERT: int
    MAX_DISK_PERCENT_ALERT: int

metric_config = MetricConfig()
