import stockfish
import chess
import requests


board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("/app/stockfish/stockfish-ubuntu-x86-64-avx2")

while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result.move)
    board.push(result.move)

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