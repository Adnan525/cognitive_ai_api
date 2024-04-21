from flask import Flask, request, jsonify
import json
import time

from llm_model import get_explanantion

all_moves = ""

llm_listen_app = Flask(__name__)

@llm_listen_app.route('/rl_move', methods=['POST'])
def get_move():
    global all_moves
    
    data = request.get_json()
    rl_move = data["move"]
    print("========================================")
    print(f"Received PGN move : {rl_move}")
    if all_moves == "":
        all_moves+=rl_move
    else:
        all_moves+=f" {rl_move}"
    # print("Generating explanation using LLM model")
    # print(get_explanantion(all_moves))
    print("Sending ack for next move")
    print("========================================")
    return "", 200

@llm_listen_app.route("/get_exp", methods=['POST'])
def get_prompt():
    data = request.get_json()
    prompt = data["prompt"]
    print("========================================")
    print(f"Received prompt : {prompt}")
    print("Generating explanation using LLM model")
    explanation_text = get_explanantion(prompt)
    print(explanation_text)
    print("Sending ack 200")
    print("========================================")
    return explanation_text, 200

# if __name__ == '__main__':
#     llm_listen_app.run(debug=True)