from pathlib import Path
from datetime import datetime
import traceback

from .logger import get_logger
import yaml

logger = get_logger(__name__)

def handle_exception(page, error, context="エラー"):
    """
    共通例外処理
    - スクリーンショット保存
    - URL / タイトル / HTML断片のログ
    - トレースログ
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = Path("logs/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    # page があるときだけスクショ
    if page is not None:
        try:
            screenshot_path = screenshot_dir / f"{context}_{timestamp}.png"
            page.screenshot(path=str(screenshot_path))
            logger.error(f"[{context}] スクリーンショット保存: {screenshot_path}")
        except Exception as ss_error:
            logger.error(f"[{context}] スクリーンショット保存に失敗: {ss_error}")
    else:
        logger.error(f"[{context}] page が None のためスクリーンショット省略")

    # page があるときだけ URL/タイトル/HTML を出す
    if page is not None:
        try:
            logger.error(f"[{context}] 現在のURL: {page.url}")
            logger.error(f"[{context}] ページタイトル: {page.title()}")
            html = page.content()
            logger.error(f"[{context}] HTML先頭500文字:\n{html[:500]}")
        except Exception as info_error:
            logger.error(f"[{context}] ページ情報取得に失敗: {info_error}")
    else:
        logger.error(f"[{context}] page が None のためページ情報省略")

    # 例外内容
    logger.error(f"[{context}] 例外: {error}")
    logger.error(traceback.format_exc())

