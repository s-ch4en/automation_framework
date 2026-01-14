from pathlib import Path
import yaml
from playwright.sync_api import sync_playwright
from .logger import get_logger

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"
logger = get_logger(__name__)


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def create_browser():
    """
    Playwright のブラウザ・コンテキスト・ページを生成して返す共通関数。
    settings.yaml の browser_type / headless を参照する。
    """
    settings = load_settings()
    browser_type = settings.get("browser", {}).get("type", "chromium")
    headless = settings.get("browser", {}).get("headless", True)

    playwright = sync_playwright().start()

    # ブラウザ選択
    if browser_type == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        logger.warning(f"Unknown browser type: {browser_type}, fallback to chromium")
        browser = playwright.chromium.launch(headless=headless)

    context = browser.new_context()
    page = context.new_page()

    logger.info(f"ブラウザ起動: {browser_type}, headless={headless}")

    return browser, context, page


class BrowserSession:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        settings = load_settings()
        self.playwright = sync_playwright().start()

        browser_type = settings.get("browser", "chromium")
        headless = settings.get("headless", True)

        if browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=headless)
        else:
            logger.warning(f"Unknown browser type: {browser_type}, fallback to chromium")
            self.browser = self.playwright.chromium.launch(headless=headless)

        self.page = self.browser.new_page()
        self.page.set_default_timeout(settings.get("timeout", 10) * 1000)
        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()