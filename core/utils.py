from playwright.sync_api import Page
from .logger import get_logger

logger = get_logger(__name__)


def fill_and_log(page: Page, selector: str, value: str, field_name: str = ""):
    logger.info(f"{field_name or selector} に値を入力: {value}")
    page.fill(selector, value)


def click_and_log(page: Page, selector: str, element_name: str = ""):
    logger.info(f"{element_name or selector} をクリック")
    page.click(selector)

def safe_fill(page: Page, selector: str, value: str, name: str = ""):
    """
    安定した入力処理（待機 + ログ付き）
    """
    logger.info(f"{name or selector} に値を入力します")
    page.wait_for_selector(selector)
    page.fill(selector, value)
