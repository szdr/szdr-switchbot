import os
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

import functions_framework
from dotenv import load_dotenv

from slack import notify_slack
from switchbot_api import SwitchBotAPIRepository
from switchbot_db import SwitchBotDBRepository

load_dotenv()


@functions_framework.cloud_event
def main(cloud_event):
    switchbot_token = os.getenv("SWITCHBOT_TOKEN")
    if switchbot_token is None:
        raise RuntimeError("SWITCHBOT_TOKEN is not set.")

    switchbot_secret = os.getenv("SWITCHBOT_SECRET")
    if switchbot_secret is None:
        raise RuntimeError("SWITCHBOT_SECREt is not set.")

    database_host = os.getenv("DATABASE_HOST")
    if database_host is None:
        raise RuntimeError("DATABASE_HOST is not set.")

    database_username = os.getenv("DATABASE_USERNAME")
    if database_username is None:
        raise RuntimeError("DATABASE_USERNAME is not set.")

    database_password = os.getenv("DATABASE_PASSWORD")
    if database_password is None:
        raise RuntimeError("DATABASE_PASSWORD is not set.")

    database = os.getenv("DATABASE")
    if database is None:
        raise RuntimeError("DATABASE is not set.")

    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url is None:
        raise RuntimeError("SLACK_WEBHOOK_URL is not set.")

    switchbot_api_repository = SwitchBotAPIRepository(switchbot_token, switchbot_secret)
    switchbot_db_repository = SwitchBotDBRepository(
        database_host, database_username, database_password, database
    )

    try:
        devices = switchbot_api_repository.get_devices()
    except Exception as e:
        stack_trace = traceback.format_exc()
        notify_slack(webhook_url, "switchbot", stack_trace)
        raise e

    log_datetime = datetime.now(tz=ZoneInfo("Asia/Tokyo"))
    for device in devices:
        try:
            status = switchbot_api_repository.get_status(device.device_id)
            switchbot_db_repository.insert(log_datetime, device, status)
        except Exception:
            # 特定のデバイスのstatus取得およびDB格納に失敗しても処理を継続する
            stack_trace = traceback.format_exc()
            notify_slack(webhook_url, "switchbot", stack_trace)


if __name__ == "__main__":
    main(None)
