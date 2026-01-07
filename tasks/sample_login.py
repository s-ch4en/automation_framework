from pathlib import Path
import yaml

from core.driver_factory import BrowserSession
from core.exception_handler import handle_exception
from core.logger import get_logger
from core.utils import fill_and_log, click_and_log, safe_fill

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"
logger = get_logger(__name__)


def load_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_login_task():
    settings = load_settings()
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

            try:
                safe_fill(page, "#username", username, "ユーザーID")
                safe_fill(page, "#password", password, "パスワード")
            except Exception as e:
                handle_exception(page, e, "入力処理失敗")
                return

            click_and_log(page, "#login-button", "ログインボタン")


            # ログイン成功の確認例（成功メッセージや要素など）
            # page.wait_for_timeout(2000)
            # logger.info("ログイン処理完了（暫定）")

            # 成功判定（例：ダッシュボードの要素を待つ）
            try:
                page.wait_for_selector("#inventory_container", timeout=5000)
                logger.info("ログイン成功を確認")
            except:
                logger.warning("ログイン成功要素が見つからず。暫定成功扱い")



        except Exception as e:
            handle_exception(page, e, context="ログインタスク")
            # 必要に応じて再スロー or 正常終了扱いの判断
            # raise


if __name__ == "__main__":
    run_login_task()