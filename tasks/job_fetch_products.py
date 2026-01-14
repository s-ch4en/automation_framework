from core.logger import get_logger
from core.driver_factory import create_browser
from core.utils import safe_fill, safe_click, check_success
from core.exception_handler import handle_exception
from core.files_util import write_csv
from core.driver_factory import load_settings

import pandas as pd
from datetime import datetime
from pathlib import Path

logger = get_logger(__name__)


def run_fetch_products():
    """
    saucedemo の商品一覧を取得して CSV に保存する処理
    job_runner から呼ばれる前提
    """
    settings = load_settings()
    url = settings["target_url"]
    username = settings["login"]["username"]
    password = settings["login"]["password"]

    browser, context, page = create_browser()

    try:
        logger.info("=== 商品一覧取得ジョブ開始 ===")

        # 1. ログインページへアクセス
        page.goto(url)
        logger.info(f"アクセス: {url}")

        # 2. ログイン
        safe_fill(page, "#user-name", username, "ユーザーID")
        safe_fill(page, "#password", password, "パスワード")
        safe_click(page, "#login-button", "ログインボタン")

        # 3. 成功判定
        check_success(page, "#inventory_container", "ログイン成功判定")

        # 4. 商品一覧を取得
        logger.info("商品一覧を取得します")

        items = page.query_selector_all(".inventory_item")
        data = []

        for item in items:
            name = item.query_selector(".inventory_item_name").inner_text()
            price = item.query_selector(".inventory_item_price").inner_text()
            data.append({"name": name, "price": price})

        df = pd.DataFrame(data)
        logger.info(f"{len(df)} 件の商品を取得")

        # 5. CSV 保存
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        filename = output_dir / f"products_{datetime.now().strftime('%Y%m%d')}.csv"
        write_csv(df, filename)

        logger.info(f"CSV 保存完了: {filename}")

        logger.info("=== 商品一覧取得ジョブ正常終了 ===")
        return 0

    except Exception as e:
        handle_exception(page, e, context="商品一覧取得ジョブ失敗")
        logger.error("=== 商品一覧取得ジョブ異常終了 ===")
        return 1

    finally:
        context.close()
        browser.close()


def main():
    return run_fetch_products()


if __name__ == "__main__":
    exit(main())