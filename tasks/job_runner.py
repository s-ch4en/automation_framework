from core.logger import get_logger
from core.job_lock import JobLock
from core.job_history import append_job_history
from core.job_loader import load_jobs
from core.notifier import notify_slack

import multiprocessing
import time

logger = get_logger(__name__)


def run_with_timeout(func, timeout):
    """
    関数を別プロセスで実行し、timeout 秒で強制終了する
    """
    def target(queue):
        try:
            result = func()
            queue.put(result)
        except Exception as e:
            queue.put(e)

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=target, args=(queue,))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return "TIMEOUT"

    result = queue.get()

    if isinstance(result, Exception):
        raise result

    return result


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
            timeout = job.get("timeout", None)
            retry = job.get("retry", 0)

            logger.info(f"=== ジョブ開始: {name} ===")

            attempt = 0
            success = False

            while attempt <= retry:
                attempt += 1
                logger.info(f"{name}: 実行試行 {attempt}/{retry+1}")

                try:
                    if timeout:
                        result = run_with_timeout(func, timeout)
                        if result == "TIMEOUT":
                            raise TimeoutError(f"{name} が {timeout} 秒でタイムアウト")
                    else:
                        result = func()

                    if result == 0:
                        logger.info(f"=== ジョブ正常終了: {name} ===")
                        append_job_history(name, "SUCCESS")
                        success = True
                        break
                    else:
                        raise Exception(f"exit code {result}")

                except Exception as e:
                    logger.error(f"{name}: エラー発生: {e}", exc_info=True)

                    if attempt > retry:
                        logger.error(f"=== ジョブ異常終了: {name} ===")
                        append_job_history(name, "FAILED", str(e))
                        notify_slack(f"❌ ジョブ失敗: {name}\n{e}")
                        exit_code = 1

            logger.info(f"=== ジョブ終了: {name} ===")

    finally:
        lock.release()
        logger.info("=== ジョブランナー終了 ===")

    return exit_code


if __name__ == "__main__":
    exit(main())