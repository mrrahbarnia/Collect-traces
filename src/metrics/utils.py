import logging

from src.metrics.config import metric_config

logger = logging.getLogger("metrics")

async def send_email(content: str) -> None:
    # Simulate sending email
    logger.info(f"{content} => Sending to => {metric_config.ADMIN_EMAIL}")
