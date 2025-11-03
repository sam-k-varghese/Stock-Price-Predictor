from loguru import logger
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logger globally
logger.add(
    "logs/app.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

__all__ = ["logger"]
