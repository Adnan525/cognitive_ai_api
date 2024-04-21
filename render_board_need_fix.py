import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
from MyChess import MyChess

from chess_engine_api import send_move

# RL engine
import chess
import chess.engine

# asynch api
import asyncio
import threading

# llm listen
from llm_listen_api import llm_listen_app

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-ubuntu-x86-64-avx2")


def convert_svg_to_png(svg_file, png_file):  # Tkinter not working with svg
    with open(svg_file, "rb") as f:
        svg_data = f.read()
    png_data = cairosvg.svg2png(bytestring=svg_data, output_width=300, output_height=300)
    with open(png_file, "wb") as f:
        f.write(png_data)


def render_move_text(moves: str):
    moves_list = moves.split()
    side = "White" if len(moves_list) % 2 == 1 else "White"
    prevs = "\n"
    for i, move in enumerate(moves_list[:-1]):
        prevs += f"{move} "
        if (i + 1) % 2 == 0:
            prevs += "\n"
    return f"Current move : {side, moves_list[-1]} \nPrevious moves : {prevs}"


class ChessBoard(tk.Tk):
    def __init__(self, state: MyChess):
        super().__init__()
        self.title("Cognitive Chess")
        self.geometry("600x600")
        
        # convert
        convert_svg_to_png("board.svg", "board.png")
        self.image = Image.open("board.png")
        self.photo = ImageTk.PhotoImage(self.image)
        
        # GUI Components
        self.create_widgets(state)
        
        
    def create_widgets(self, state: MyChess):
        
        # grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Chess Board Display
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.grid(row=0, column=1, sticky="nw")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # label
        self.entry = tk.Label(self, text=render_move_text(state.moves),
                              justify="left", wraplength=400, anchor="ne", pady=80, padx = 20)
        self.entry.grid(row=1, column=1, sticky="nw")

        # User Input Text Box
        self.user_label = tk.Label(self, text="User:")
        self.user_label.grid(row=1, column=0, sticky="nw")
        self.user_input = tk.Text(self, width=50, height=13, pady=20)
        self.user_input.grid(row=1, column=0, sticky="sw")
        
        # Buttons
        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, sticky="ew")

        self.next_move_button = tk.Button(self, text="Next Move", command=self.play_next_move)
        self.next_move_button.grid(row=2, column=1, sticky="ew")

        self.prompt_button = tk.Button(self, text="Generate Prompt", command=self.generate_prompt)
        self.prompt_button.grid(row=3, column=0, sticky="ew")

        self.explanation_button = tk.Button(self, text="Get Explanation", command=self.get_explanation)
        self.explanation_button.grid(row=3, column=1, sticky="ew")

    def run_flask_app(self):
        llm_listen_app.run()
        
    def start_game(self):
        # Create a thread to run the Flask app
        self.flask_thread = threading.Thread(target=self.run_flask_app)
        self.flask_thread.start()
        self.start_button.config(state=tk.DISABLED)

    def play_next_move(self):
        # Play the next move logic here
        send_move(board, engine)
        pass

    def generate_prompt(self):
        # Generate prompt logic here
        self.user_input.delete('1.0', tk.END)
        self.user_input.insert(tk.END, "What is the rationale behind the previous move")
    def get_explanation(self):
        # Get explanation logic here
        previous_move = self.state.moves.split()[-1]
        # explanation = send_moves(previous_move, "http://127.0.0.1:5000/rl_move")  # Assuming this function sends the move to LLM and returns the explanation


if __name__ == "__main__":
    moves = "d4 Nf6 c4 c5 e3 cxd4 exd4 d5 Nf3"
    gui_app = ChessBoard(MyChess(moves))
    gui_app.mainloop()