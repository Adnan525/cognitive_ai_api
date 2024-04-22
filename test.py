from send_move_api import url, send_moves

print(send_moves("e2e4", "http://127.0.0.1:5000/rl_move"))
# import tkinter as tk
# from PIL import Image, ImageTk

# class MyApp(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("PNG Image Viewer")

#         # Initial load of the PNG image
#         self.load_image()

#         # Create a canvas
#         self.canvas = tk.Canvas(self, width=self.image.width, height=self.image.height)
#         self.canvas.grid(row=0, column=0, sticky="nw")

#         # Display the initial image on the canvas
#         self.photo = ImageTk.PhotoImage(self.image)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

#         # Create a button to update the image
#         self.update_button = tk.Button(self, text="Update Image", command=self.update_image)
#         self.update_button.grid(row=1, column=0, pady=10)

#     def load_image(self):
#         # Load the PNG image
#         self.image = Image.open("board.png")

#     def update_image(self):
#         # Reload the PNG image
#         self.load_image()

#         # Convert the reloaded image to PhotoImage and update the canvas
#         self.photo = ImageTk.PhotoImage(self.image)
#         self.canvas.config(width=self.image.width, height=self.image.height)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

# if __name__ == "__main__":
#     app = MyApp()
#     app.mainloop()
# from render_board_needs_fix import convert_svg_to_png
# from MyChess import MyChess
# MyChess("d4 d6 Bf4 e5 Bg3 Nf6 e3 exd4 exd4 d5 c3 Bd6 Bd3 O-O Nd2 Re8+ Kf1 Bxg3 hxg3 b6 g4 Ba6 g5 Bxd3+ Ne2 Ne4 Nxe4 Bxe4 Nf4 Qxg5 Nh3 Bxg2+ Kg1 Qg6 Nf4 Qg5 Nxg2 Re6 Qd3 Rh6 Qe2 Nc6 Re1 g6 f4 Rxh1+ Kxh1 Qh6+ Kg1 a5 Qb5 Na7 Re8+ Rxe8 Qxe8+ Kg7 Qe5+ Kg8 Qxc7 Qh5 Qxa7 Qd1+ Kh2 Qa1 Nh4 Qxb2+ Kh3 Qxc3+ Kg4 Qxd4 Qb8+ Kg7 Nf3 Qa1 Kg5 Qxa2 Ne5 Qg2+ Kh4 h5 Nxf7 Qg4#")
# convert_svg_to_png("board.svg", "test.png")