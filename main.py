import requests
import json
from LLMengine import LLM_out_texts, accounts

def send_to_dingtalk(message, webhook):
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }

    try:
        response = requests.post(
            webhook,
            headers=headers,
            data=json.dumps(data)
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    for i, message in enumerate(LLM_out_texts):
        print(message)
        send_result = send_to_dingtalk(message, accounts[i]["dingtalk_webhook"])
        print(f"钉钉发送结果 (账户 {i+1}):", send_result)