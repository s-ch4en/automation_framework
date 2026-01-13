from pathlib import Path
import os
import time

LOCK_FILE = Path("job.lock")

class JobLock:
    """
    多重起動防止のためのロックファイル管理
    """

    def __init__(self, lock_path: Path = LOCK_FILE):
        self.lock_path = lock_path

    def acquire(self) -> bool:
        """
        ロック取得
        すでにロックがあれば False を返す
        """
        if self.lock_path.exists():
            return False

        # ロックファイル作成
        self.lock_path.write_text(str(time.time()))
        return True

    def release(self):
        """
        ロック解除
        """
        if self.lock_path.exists():
            os.remove(self.lock_path)
