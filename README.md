# API for Cognitive AI

Using a flask API to establish comm between the RL chess engine and and LLM model. At this stage chess engine is working fine and little to no modification is required. The listening code of the API will be added to the model_loading code. llm_model.py is a dummy explanation function that just waits 10 seconds to mimic LLM inference for now.

## Installation

Check requirements.txt, a docker container will be pushed to dockerhub and the link will be added here.

## Test phase
![3_move_test](https://github.com/Adnan525/cognitive_ai_api/blob/master/api_test_3_moves.png)  

## GUI Support
![GUI](https://github.com/Adnan525/cognitive_ai_api/blob/master/gui_support.png)  
  
- Start game starts the LLM listen api which repnds to /rl_move and /get_exp. Since we have a GUI running, this has to be started in a different thread  
- Next Move takes move from StockFish and sends it to LLM listen, meanwhile we capture it in the GUI file and show it on GUI, also kept a list of all the moves  
- Generate prompt takes the list of current moves and generate the prompt  
- Get explanation used a dummy LLM model and sends used input to the model  

## License

[MIT](https://choosealicense.com/licenses/mit/)