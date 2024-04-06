import requests
import json

# flask api endpoint port 5000
url = "http://127.0.0.1:5000/rl_move"

# test string
move = "e2e4"

# payload for the POST request
payload = {"move": move}

# send POST request 
response = requests.post(url, json=payload)

if response.status_code == 200:
    print("OK")
else:
    print("Error:", response.status_code)