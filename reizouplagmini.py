import requests
import time
import uuid
import hmac
import hashlib
import base64

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

# トークンとシークレットキーを設定
api_token = 'b49874c4f3af64b1e6bb754bc10a703ec441878739bfd549642f5d4041e271a2bf7834cf27a8969af5b909d558d1e7e1'
secret_token = '1d58b22e63cd0e2a1075677ab6085de7'
device_id = '6055F927277E'

# 30分ごとにON/OFFを切り替える
while True:
    # プラグ電源オフ
    send_command(api_token, secret_token, device_id, "turnOff")
    time.sleep(30 * 60)  # 30分待機

    # プラグ電源オン
    send_command(api_token, secret_token, device_id, "turnOn")
    time.sleep(30 * 60)  # 30分待機
