import json

import requests


def notify_slack(webhook_url: str, header: str, message: str):
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": f"{header}"}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Details:*\n```{message}```"},
            },
        ]
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return response.status_code
