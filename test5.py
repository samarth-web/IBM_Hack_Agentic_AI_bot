import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_message(text):
    payload = {
        "text": text
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("✅ Sent Slack message")
    else:
        print(f"❌ Slack error: {response.status_code} {response.text}")
task_summary = "✅ Trello card created: Finalize Product Launch Timeline"
send_slack_message(task_summary)
