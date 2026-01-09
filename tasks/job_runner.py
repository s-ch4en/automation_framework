from core.logger import get_logger
from tasks.job_sample_login import main as job_sample_login

logger = get_logger(__name__)


def main() -> int:
    logger.info("=== ジョブランナー開始 ===")
    exit_code = 0

    # 1つ目のジョブ
    code = job_sample_login()
    if code != 0:
        logger.error(f"job_sample_login が異常終了 (exit_code={code})")
        exit_code = code  # ここでは最初のエラーコードを採用

    logger.info("=== ジョブランナー終了 ===")
    return exit_code


if __name__ == "__main__":
    exit(main())