from core.logger import get_logger
from tasks.sample_login import run_login_task

logger = get_logger(__name__)


def main() -> int:
    """
    ジョブエントリポイント
    戻り値を終了コードとして OS に返す想定
    """
    logger.info("=== ジョブ開始: sample_login ===")
    try:
        run_login_task()
        logger.info("=== ジョブ正常終了: sample_login ===")
        return 0  # 成功
    except Exception as e:
        logger.error("=== ジョブ異常終了: sample_login ===", exc_info=True)
        # ここで Slack 通知やメール送信などを後で足せる
        return 1  # 失敗


if __name__ == "__main__":
    exit(main())