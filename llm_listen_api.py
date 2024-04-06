from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

@app.route('/rl_move', methods=['POST'])
def get_move():
    data = request.get_json()
    rl_move = data["move"]

    print(f"Received PGN move : {rl_move}")
    print("testing 5s delay")
    time.sleep(5)
    print("active now, returning 200")
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)