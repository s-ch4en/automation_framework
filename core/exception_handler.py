from pathlib import Path
from datetime import datetime
import traceback

from .logger import get_logger
import yaml

logger = get_logger(__name__)
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def handle_exception(page, error: Exception, context: str = ""):
    settings = load_settings()
    screenshot_dir = Path(settings["screenshot_dir"])
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = screenshot_dir / f"{context}_{timestamp}.png"

    try:
        if page:
            page.screenshot(path=str(screenshot_path), full_page=True)
            logger.error(f"[{context}] エラー発生。スクリーンショット保存: {screenshot_path}")
    except Exception as e:
        logger.error(f"スクリーンショット取得に失敗: {e}")

    logger.error(f"[{context}] 例外: {error}")
    logger.error(traceback.format_exc())