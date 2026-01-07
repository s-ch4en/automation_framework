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
    logger.info(f"{label} に値を入力します")
    try:
        page.wait_for_selector(selector)
        page.fill(selector, value)
    except Exception as e:
        handle_exception(page, e, context=f"{label}入力失敗")
        raise

def safe_click(page: Page, selector: str, name: str = ""):
    """
    安定したクリック処理（待機 + ログ付き）

    :param page: Playwright の Page オブジェクト
    :param selector: クリック対象のセレクタ
    :param name: 人間に分かりやすい要素名（例: "ログインボタン"）
    """
    label = name or selector
    logger.info(f"{label} をクリックします")

    try:
        page.wait_for_selector(selector)
        page.click(selector)
    except Exception as e:
        handle_exception(page, e, context=f"{label}クリック失敗")
        raise


def check_success(page, selector: str, name="成功判定"):
    logger.info(f"{name}: {selector} を待機中…")
    try:
        page.wait_for_selector(selector, timeout=5000)
        logger.info(f"{name}: 成功")
        return True
    except Exception as e:
        logger.error(f"{name}: 要素が見つからず失敗")
        logger.error(f"使用したセレクタ: {selector}")
        logger.error(f"現在のURL: {page.url}")
        logger.error(f"ページタイトル: {page.title()}")

        html = page.content()
        logger.error(f"HTML先頭500文字:\n{html[:500]}")

        ids = page.eval_on_selector_all("*", "els => els.map(e => e.id).filter(id => id)")
        logger.error(f"ページ内のID一覧: {ids}")


        handle_exception(page, e, context=f"{name}失敗")
        return False
