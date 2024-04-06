from flask import Flask, request, jsonify
import json


app = Flask(__name__)

@app.route('/rl_move', methods=['POST'])
def get_move():
    data = request.get_json()
    rl_move = data["move"]

    print(f"Received PGN move : {rl_move}")
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)