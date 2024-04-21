import chess
import chess.engine

from send_move_api import url, send_moves

def send_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(f"Selected move from stockfish {result.move.uci()}")
    board.push(result.move)
    send_moves(result.move.uci(), url)
    return result.move.uci()