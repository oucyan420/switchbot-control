import os
import requests
import time
import uuid
import hmac
import hashlib
import base64

# 環境変数からトークンとシークレットキーを読み込む
api_token = os.getenv('API_TOKEN')
secret_token = os.getenv('SECRET_TOKEN')
device_id = os.getenv('DEVICE_ID')

def send_command(api_token, secret_token, device_id, command):
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    t = int(time.time() * 1000)
    nonce = str(uuid.uuid4())
    string_to_sign = f"{api_token}{t}{nonce}".encode('utf-8')
    secret_key = secret_token.encode('utf-8')
    signature = hmac.new(secret_key, string_to_sign, hashlib.sha256).digest()
    sign = base64.b64encode(signature).decode('utf-8').upper()

    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json",
        "t": str(t),
        "nonce": nonce,
        "sign": sign
    }

    body = {
        "command": command,
        "parameter": "default",
        "commandType": "command"
    }

    response = requests.post(url, headers=headers, json=body)
    print(f"Sending {command} command: {response.text}")

# 30分ごとにON/OFFを切り替える
while True:
    # プラグ電源オン
    send_command(api_token, secret_token, device_id, "turnOn")
    time.sleep(30 * 60)  # 30分待機

    # プラグ電源オフ
    send_command(api_token, secret_token, device_id, "turnOff")
    time.sleep(30 * 60)  # 30分待機
