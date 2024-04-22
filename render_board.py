import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
from MyChess import MyChess

from chess_engine_api import send_move
from send_prompt_api import send_prompt, url_prompt

# RL engine
import chess
import chess.engine

# asynch api
import asyncio
import threading

#llm listen
from llm_listen_api import llm_listen_app

# global variables
board = chess.Board()
stockfish_path = r"C:\Users\DELL\AppData\Local\miscApps\stockfish-windows-x86-64-avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
rec_moves = ""

# utils
from utils import render_move_text, generate_prompt, prepare

def convert_svg_to_png(svg_file, png_file):
    with open(svg_file, "rb") as f:
        svg_data = f.read()
    png_data = cairosvg.svg2png(bytestring=svg_data, output_width=300, output_height=300)
    with open(png_file, "wb") as f:
        f.write(png_data)


class ChessBoard(tk.Tk):

    def __init__(self, state: MyChess):
        super().__init__()
        self.title("Cognitive Chess")
        self.geometry("600x620")
        
        # convert
        convert_svg_to_png("board.svg", "board.png")
        self.image = Image.open("board.png")
        self.photo = ImageTk.PhotoImage(self.image)
        
        # GUI Components
        self.create_widgets(state)
        
        
    def create_widgets(self, state: MyChess):

        global rec_moves
        
        # grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Chess Board Display
        self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
        self.canvas.grid(row=0, column=1, sticky="nw")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)



        # # label
        # self.entry = tk.Label(self, text=render_move_text(rec_moves),
        #                       justify="left", wraplength=400, anchor="ne", pady=80, padx = 20)
        # self.entry.grid(row=1, column=1, sticky="nw")
        
        # Frame to display text of chess moves
        moves_frame = tk.Frame(self)
        moves_frame.grid(row=1, column=1, sticky="nw")
        
        # Label
        moves_label = tk.Label(moves_frame, text="Chess Moves (Algebraic Form):")
        moves_label.grid(row=0, column=0, sticky="w")        
        
        # Text 
        self.moves_text = tk.Text(moves_frame, wrap="word", width=35, height=15, state="disabled")
        self.moves_text.grid(row=1, column=0, sticky="nw")   
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(moves_frame, orient="vertical", command=self.moves_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure text widget to use scrollbar
        self.moves_text.config(yscrollcommand=self.scrollbar.set)
        
        # Insert moves text into the text widget
        self.moves_text.insert(tk.END, render_move_text(state.moves))



        # # User Input Text Box
        # self.user_label = tk.Label(self, text="User:")
        # self.user_label.grid(row=1, column=0, sticky="nw")
        # self.user_input = tk.Text(self, width=50, height=13, pady=20)
        # self.user_input.grid(row=1, column=0, sticky="sw")
        
        # Frame to display prompt/user input
        user_frame = tk.Frame(self)
        user_frame.grid(row=1, column=0, sticky="nw")
        
        # Label
        self.user_label = tk.Label(user_frame, text="User:")
        self.user_label.grid(row=0, column=0, sticky="w")
        
        # User input box
        self.user_input = tk.Text(user_frame, wrap="word", width=35, height=15)
        self.user_input.grid(row=1, column=0, sticky="nw")
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(user_frame, orient="vertical", command=self.user_input.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure text widget to use scrollbar
        self.user_input.config(yscrollcommand=self.scrollbar.set)



        # # text box
        # self.generated_text_box = tk.Text(self, width=50, height=10, wrap="word", pady=10, padx=10)
        # self.generated_text_box.grid(row=0, column = 0, sticky="nsew")
        
        # Frame to display AI cognitive response 
        resp_frame = tk.Frame(self)
        resp_frame.grid(row=0, column=0, sticky="nw")
        
        # Label
        self.resp_label = tk.Label(resp_frame, text="Response")
        self.resp_label.grid(row=0, column=0, sticky="w")
        
        self.resp_text = tk.Text(resp_frame, width=35, height=18, wrap="word")
        self.resp_text.grid(row=1, column = 0, sticky="nw")
        
        # Scrollbar
        self.scrollbar = tk.Scrollbar(resp_frame, orient="vertical", command=self.resp_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Configure text widget to use scrollbar
        self.resp_text.config(yscrollcommand=self.scrollbar.set)
        
        
        
        # Buttons
        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, sticky="ew")

        self.next_move_button = tk.Button(self, text="Next Move", command=self.play_next_move)
        self.next_move_button.grid(row=2, column=1, sticky="ew")

        self.prompt_button = tk.Button(self, text="Generate Prompt", command=self.generate_prompt)
        self.prompt_button.grid(row=3, column=0, sticky="ew")

        self.explanation_button = tk.Button(self, text="Get Explanation", 
                                            command= self.get_explanation_and_update_text)
        self.explanation_button.grid(row=3, column=1, sticky="ew")

    
    def run_flask_app(self):
        llm_listen_app.run()
        
    def start_game(self):
        # creating a thread to run the Flask app, otherwise GUI will freeze
        self.flask_thread = threading.Thread(target=self.run_flask_app)
        self.flask_thread.start()
        self.start_button.config(state=tk.DISABLED)

        self.resp_text.insert(tk.END, "------LLM API CONNECTED-------" + "\n")

    def play_next_move(self):
        global rec_moves
        rec_moves += send_move(board, engine) + " "
        
        # Clear the existing content of the moves text widget
        self.moves_text.config(state="normal")  # Set state to normal to enable editing
        self.moves_text.delete("1.0", tk.END)   # Delete all content
        self.moves_text.insert(tk.END, render_move_text(rec_moves))  # Insert new moves text
        self.moves_text.config(state="disabled")  # Set state back to disabled
        
        # # refresh the label text
        # self.moves_text.insert(tk.END, render_move_text(rec_moves))
        # # print(f"==========================>{rec_moves}")

    def generate_prompt(self):
        self.user_input.delete('1.0', tk.END)
        self.user_input.insert(tk.END, generate_prompt(rec_moves))


    def get_explanation_and_update_text(self):
        # Update user text immediately
        user_text = self.user_input.get("1.0", tk.END)
        self.resp_text.insert(tk.END, f"USER : {user_text}" + "\n")

        # schedule explanation retrieval after a short delay
        self.after(500, lambda: self._get_explanation_and_update(user_text))

    def _get_explanation_and_update(self, user_text):
        explanation = send_prompt(prepare(user_text, rec_moves), url_prompt)
        self.resp_text.insert(tk.END, f"ASSISTANT : {explanation}" + "\n")

    # def get_explanation(self):
    #     self.update_text()
    #     user_text = self.user_input.get("1.0", tk.END)
    #     explanation = send_prompt(user_text, url_prompt)
    #     self.generated_text_box.insert(tk.END, f"ASSISTANT : {explanation}" + "\n")

    # def update_text(self):
    #     user_text = self.user_input.get("1.0", tk.END)
    #     self.generated_text_box.insert(tk.END, f"USER : {user_text}" + "\n")

if __name__ == "__main__":
    moves = ""
    gui_app = ChessBoard(MyChess(moves))
    gui_app.mainloop()