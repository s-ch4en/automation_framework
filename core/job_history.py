import csv
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("logs/job_history.csv")

def append_job_history(job_name: str, status: str, message: str = ""):
    """
    ジョブ実行履歴を CSV に追記する
    status: SUCCESS / FAILED
    """
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    is_new = not HISTORY_FILE.exists()

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # 初回はヘッダを書く
        if is_new:
            writer.writerow(["timestamp", "job_name", "status", "message"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            job_name,
            status,
            message
        ])