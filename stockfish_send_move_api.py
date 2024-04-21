import stockfish
import chess
import chess.engine
import requests

from send_move_api import url, send_moves

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-ubuntu-x86-64-avx2")

# testing for 3 move
count = 0
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    # result.move type is <class 'chess.Move'>
    # print(type(result.move.uci()))
    print(f"Selected move from stockfish {result.move.uci()}")
    board.push(result.move)
    send_moves(result.move.uci(), url)

    # test
    count+=1
    if count == 3:
        break


# optional
if board.is_checkmate():
    if board.turn == chess.WHITE:
        print("Black wins by checkmate!")
    else:
        print("White wins by checkmate!")
elif board.is_stalemate():
    print("Stalemate!")
elif board.is_insufficient_material():
    print("Draw due to insufficient material!")
elif board.is_seventyfive_moves():
    print("Draw due to 75-move rule!")
elif board.is_fivefold_repetition():
    print("Draw due to fivefold repetition!")

engine.quit()