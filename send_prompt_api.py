import requests
import json

# flask api endpoint port 5000
url_prompt = "http://127.0.0.1:5000/get_exp"

def send_prompt(prompt: str, url: str, timeout: float = 15):
    payload = {"prompt": prompt}
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        if response.status_code == 200:
            explanation_text = response.text
            return explanation_text
        else:
            return "Failed"
    except requests.Timeout:
        return "Timeout"