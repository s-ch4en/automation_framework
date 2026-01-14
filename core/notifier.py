import requests
from core.logger import get_logger
from core.driver_factory import load_settings

logger = get_logger(__name__)

def notify_slack(message: str):
    settings = load_settings()
    webhook = settings.get("slack_webhook_url")

    if not webhook:
        logger.warning("Slack Webhook URL が設定されていません")
        return

    payload = {"text": message}

    try:
        requests.post(webhook, json=payload, timeout=5)
        logger.info("Slack 通知送信完了")
    except Exception as e:
        logger.error(f"Slack 通知送信失敗: {e}")