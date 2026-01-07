import logging
from logging import handlers
from pathlib import Path
import yaml
from logging.handlers import RotatingFileHandler

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str) -> logging.Logger:
    settings = load_settings()
    log_dir = Path(settings["log_dir"])
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(settings.get("log_level", "INFO"))

    # 重複防止
    if logger.hasHandlers():
        logger.handlers.clear()

    log_file = log_dir / "automation.log"

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
