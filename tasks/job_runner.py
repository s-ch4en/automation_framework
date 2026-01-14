from core.logger import get_logger
from core.job_lock import JobLock
from core.job_history import append_job_history
from core.job_loader import load_jobs
from core.notifier import notify_slack

logger = get_logger(__name__)

def main() -> int:
    lock = JobLock()

    if not lock.acquire():
        logger.error("ジョブがすでに実行中のため終了します")
        notify_slack("⚠️ ジョブ多重起動検知：job_runner")
        return 1

    logger.info("=== ジョブランナー開始 ===")

    exit_code = 0

    try:
        jobs = load_jobs()

        for job in jobs:
            name = job["name"]
            func = job["func"]

            logger.info(f"=== ジョブ開始: {name} ===")

            try:
                result = func()
                if result == 0:
                    logger.info(f"=== ジョブ正常終了: {name} ===")
                    append_job_history(name, "SUCCESS")
                else:
                    logger.error(f"=== ジョブ異常終了: {name} (exit={result}) ===")
                    append_job_history(name, "FAILED", f"exit={result}")
                    notify_slack(f"❌ ジョブ失敗: {name} (exit={result})")
                    exit_code = result

            except Exception as e:
                logger.error(f"=== ジョブ異常終了: {name} ===", exc_info=True)
                append_job_history(name, "FAILED", str(e))
                notify_slack(f"❌ ジョブ例外発生: {name}\n{e}")
                exit_code = 1

    finally:
        lock.release()
        logger.info("=== ジョブランナー終了 ===")

    return exit_code


if __name__ == "__main__":
    exit(main())
