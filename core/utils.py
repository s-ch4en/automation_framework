from playwright.sync_api import Page
from .logger import get_logger
from .exception_handler import handle_exception

logger = get_logger(__name__)


def fill_and_log(page: Page, selector: str, value: str, field_name: str = ""):
    """
    Deprecated: safe_fill を使用してください
    """

    logger.info(f"{field_name or selector} に値を入力: {value}")
    page.fill(selector, value)


def click_and_log(page: Page, selector: str, element_name: str = ""):
    """
    Deprecated: safe_click を使用してください
    """

    logger.info(f"{element_name or selector} をクリック")
    page.click(selector)

def safe_fill(page: Page, selector: str, value: str, name: str = ""):
    """
    安定した入力処理（待機 + ログ付き）
    """
    label = name or selector
    logger.info(f"{label} をクリックします")
    try:
        page.wait_for_selector(selector)
        page.click(selector)
    except Exception as e:
        handle_exception(page, e, context=f"{label} クリック失敗")
        raise
