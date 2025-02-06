# slack_alert.py
import requests
from PythonCore.env_vars import get_env_var


def send_slack_alert(message):
    """Send an alert to Slack to channel"""
    slack_alert_webhook = get_env_var('SLACK_ALERT_WEBHOOK')
    production_alarm_webhook = get_env_var('PRODUCTION_ALARM_WEBHOOK')
    env = get_env_var('ENV')
    token = get_env_var('TOKEN')

    print(f"Preparing to send Slack alert: {message}")

    # Don't send unless running in prod
    if 'prod' not in env.lower():
        print("Skipping slack")
        return

    if 'error' in message.lower() or 'failed' in message.lower():
        payload = {"text": f"Error in {token} Staking Rewards File Delivery:  {message}", "mrkdwn": 'true'}
        payload = str(payload)
        requests.post(production_alarm_webhook, payload)

    payload = {"text": f"{token} Staking Rewards File Delivery:  {message}", "mrkdwn": 'true'}
    payload = str(payload)
    requests.post(slack_alert_webhook, payload)