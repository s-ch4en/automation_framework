import yaml
import importlib
from pathlib import Path

JOBS_CONFIG = Path("config/jobs.yaml")

def load_jobs():
    """
    jobs.yaml を読み込み、実行可能なジョブのリストを返す
    """
    with open(JOBS_CONFIG, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    jobs = []
    for job in config.get("jobs", []):
        if not job.get("enabled", True):
            continue

        module_name = job["module"]
        function_name = job["function"]

        module = importlib.import_module(module_name)
        func = getattr(module, function_name)

        jobs.append({
            "name": job["name"],
            "func": func
        })

    return jobs