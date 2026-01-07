from pathlib import Path
import yaml

from core.driver_factory import BrowserSession
from core.exception_handler import handle_exception
from core.logger import get_logger
from core.utils import click_and_log, safe_fill, safe_click, check_success

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"
logger = get_logger(__name__)


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_login_task():
    settings = load_settings()
    success_selector = settings["success_selector"]
    url = settings["target_url"]
    username = settings["login"]["username"]
    password = settings["login"]["password"]

    with BrowserSession() as page:
        try:
            logger.info("ログインタスク開始")

            try:
                page.goto(url)
            except Exception as e:
                handle_exception(page, e, "アクセス失敗")
                return

            logger.info("ページタイトル: " + page.title())
            logger.info(f"URL へアクセス: {url}")

            safe_fill(page, "#user-name", username, "ユーザーID")
            safe_fill(page, "#password", password, "パスワード")
            safe_click(page, "#login-button", "ログインボタン")


            # ログイン成功の確認例（成功メッセージや要素など）
            # page.wait_for_timeout(2000)
            # logger.info("ログイン処理完了（暫定）")

            # 成功判定（例：ダッシュボードの要素を待つ）
            check_success(page, success_selector, "ログイン成功判定")
            logger.info(f"ログイン後URL: {page.url}")
            logger.info(f"ログイン後タイトル: {page.title()}")

        except Exception as e:
            handle_exception(page, e, context="ログインタスク")
            # 必要に応じて再スロー or 正常終了扱いの判断
            # raise


if __name__ == "__main__":
    run_login_task()