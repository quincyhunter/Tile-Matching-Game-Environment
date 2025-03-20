import tkinter as tk
from tkinter import messagebox, ttk
from observer import Observer
import time
import sys
import os
import subprocess

# Restarts the application to return to the main menu
def restart_to_main_menu():
    python = sys.executable
    main_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    
    subprocess.Popen([python, main_script])

# Main GUI class for split-screen multiplayer manages two game instances side by side
class SplitScreenMultiplayerGUI(tk.Tk):
    def __init__(self, game_type, player1, player2):
        super().__init__()
        self.title("Multiplayer")
        self.state('zoomed')  
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.game_type = game_type
        self.player1 = player1
        self.player2 = player2
        self.running = False
        self.update_rate = 33  
        self.game_over_shown = False  
        
        self.top_bar = tk.Frame(self, bd=1, relief=tk.RAISED, bg="#e0e0e0")
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        
        self.back_button = tk.Button(
            self.top_bar, 
            text="Back to Main Menu", 
            command=self.return_to_main_menu,
            font=("Arial", 10, "bold"),
            bg="#ff9999",
            padx=10,
            pady=3,
            relief=tk.GROOVE
        )
        self.back_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        title_label = tk.Label(
            self.top_bar, 
            text=f"{self.game_type.__name__}", 
            font=("Arial", 14, "bold"),
            bg="#e0e0e0"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_player_frames()
        
        self.create_game_instances()
        
        self.bind_keys()
        
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(fill=tk.X, pady=5)
        
        self.restart_button = tk.Button(
            self.controls_frame, 
            text="Restart Games", 
            command=self.restart_games, 
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.GROOVE
        )
        self.restart_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def setup_player_frames(self):
        self.player1_frame = tk.LabelFrame(
            self.main_frame, 
            text=f"Player 1: {self.player1.name} (WASD)", 
            font=("Arial", 14, "bold"),
            bd=3,
            relief=tk.GROOVE,
            padx=10,
            pady=10,
            bg="#f0f8ff"  
        )
        self.player1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.player2_frame = tk.LabelFrame(
            self.main_frame, 
            text=f"Player 2: {self.player2.name} (Arrow Keys)", 
            font=("Arial", 14, "bold"),
            bd=3,
            relief=tk.GROOVE,
            padx=10,
            pady=10,
            bg="#fff0f8"  
        )
        self.player2_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.player1_score_var = tk.StringVar(value="Score: 0")
        self.player1_score_label = tk.Label(
            self.player1_frame, 
            textvariable=self.player1_score_var, 
            font=("Arial", 12, "bold"),
            bg="#f0f8ff"
        )
        self.player1_score_label.pack(anchor=tk.NW, pady=(0, 10))
        
        self.player2_score_var = tk.StringVar(value="Score: 0")
        self.player2_score_label = tk.Label(
            self.player2_frame, 
            textvariable=self.player2_score_var, 
            font=("Arial", 12, "bold"),
            bg="#fff0f8"
        )
        self.player2_score_label.pack(anchor=tk.NE, pady=(0, 10))
    
    def create_game_instances(self):
        if self.game_type.__name__ == "Tetris":
            self.player1_gui = PlayerTetrisGUI(self.player1_frame, self.player1, is_player1=True)
            self.player2_gui = PlayerTetrisGUI(self.player2_frame, self.player2, is_player1=False)
        else:  
            self.player1_gui = PlayerCandyCrushGUI(self.player1_frame, self.player1, is_player1=True)
            self.player2_gui = PlayerCandyCrushGUI(self.player2_frame, self.player2, is_player1=False)
        
        self.player1_game = self.game_type()
        self.player2_game = self.game_type()
        
        self.player1_game.add_player(self.player1)
        self.player2_game.add_player(self.player2)
        
        self.player1_game.register_observer(self.player1_gui)
        self.player2_game.register_observer(self.player2_gui)
        
        self.player1_game.start()
        self.player2_game.start()
        
        self.update()
    
    def restart_games(self):
        self.game_over_shown = False
        
        if hasattr(self.player1_game, 'stop'):
            self.player1_game.stop()
        if hasattr(self.player2_game, 'stop'):
            self.player2_game.stop()
            
        self.player1.update_score(-self.player1.score)  
        self.player2.update_score(-self.player2.score)  
        
        self.create_game_instances()
        
        self.restart_button.config(bg="SystemButtonFace", fg="black", font=("Arial", 10))
    
    def bind_keys(self):
        self.unbind("w")
        self.unbind("a")
        self.unbind("s")
        self.unbind("d")
        self.unbind("<space>")
        self.unbind("<Up>")
        self.unbind("<Left>")
        self.unbind("<Down>")
        self.unbind("<Right>")
        self.unbind("<Return>")
        self.unbind("<Tab>")
        self.unbind("r")
        
        self.bind("w", lambda event: self.handle_key_press(event, 1, "UP"))
        self.bind("a", lambda event: self.handle_key_press(event, 1, "LEFT"))
        self.bind("s", lambda event: self.handle_key_press(event, 1, "DOWN"))
        self.bind("d", lambda event: self.handle_key_press(event, 1, "RIGHT"))
        self.bind("<space>", lambda event: self.handle_key_press(event, 1, "SPACE"))
        
        self.p2_key_state = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False, "SPACE": False}
        #arrows were not working so added key release to prevent double movement
        self.bind("<KeyPress-Up>", lambda event: self.handle_p2_key_press(event, "UP"))
        self.bind("<KeyRelease-Up>", lambda event: self.handle_p2_key_release(event, "UP"))
        
        self.bind("<KeyPress-Down>", lambda event: self.handle_p2_key_press(event, "DOWN"))
        self.bind("<KeyRelease-Down>", lambda event: self.handle_p2_key_release(event, "DOWN"))
        
        self.bind("<KeyPress-Left>", lambda event: self.handle_p2_key_press(event, "LEFT"))
        self.bind("<KeyRelease-Left>", lambda event: self.handle_p2_key_release(event, "LEFT"))
        
        self.bind("<KeyPress-Right>", lambda event: self.handle_p2_key_press(event, "RIGHT"))
        self.bind("<KeyRelease-Right>", lambda event: self.handle_p2_key_release(event, "RIGHT"))
        
        self.bind("<KeyPress-Return>", lambda event: self.handle_p2_key_press(event, "SPACE"))
        self.bind("<KeyRelease-Return>", lambda event: self.handle_p2_key_release(event, "SPACE"))
        
        
    
    def handle_key_press(self, event, player_num, key):
        if player_num == 1:
            if hasattr(self.player1_gui, 'handle_key'):
                self.player1_gui.handle_key(key)
        elif player_num == 2:
            if hasattr(self.player2_gui, 'handle_key'):
                self.player2_gui.handle_key(key)
        
        return "break"
    
    def handle_tab_key(self):
        if self.game_type.__name__ == "CandyCrush":
            if hasattr(self.player1_game, 'handle_input'):
                self.player1_game.handle_input(99, 99)  
            if hasattr(self.player2_game, 'handle_input'):
                self.player2_game.handle_input(99, 99)  
    
    def handle_p2_key_press(self, event, key):
        if self.p2_key_state[key]:
            return "break"
            
        self.p2_key_state[key] = True
        self.handle_key_press(event, 2, key)
        return "break"
    
    def handle_p2_key_release(self, event, key):
        self.p2_key_state[key] = False
        return "break"
    
    def start_game_loop(self):
        self.running = True
        self.update_game()
    
    def update_game(self):
        if self.running:
            if hasattr(self.player1_game, 'update'):
                self.player1_game.update()
            if hasattr(self.player2_game, 'update'):
                self.player2_game.update()
            
            if self.player1:
                self.player1_score_var.set(f"Score: {self.player1.score}")
            if self.player2:
                self.player2_score_var.set(f"Score: {self.player2.score}")
            
            self.check_game_over()
            
            self.after(self.update_rate, self.update_game)
    
    def check_game_over(self):
        player1_game_over = hasattr(self.player1_game, 'game_over') and self.player1_game.game_over
        player2_game_over = hasattr(self.player2_game, 'game_over') and self.player2_game.game_over
        
        if (player1_game_over and player2_game_over) and not self.game_over_shown:
            self.game_over_shown = True
            
            winner = None
            if self.player1.score > self.player2.score:
                winner = self.player1
            elif self.player2.score > self.player1.score:
                winner = self.player2
            
            message = f"Game Over!\n\n{self.player1.name}: {self.player1.score}\n{self.player2.name}: {self.player2.score}\n\n"
            if winner:
                message += f"Winner: {winner.name}!"
            else:
                message += "It's a tie!"
            
            self.after(100, lambda: messagebox.showinfo("Game Over", message))
            
            self.restart_button.config(bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
    
    def on_close(self):
        self.running = False
        if hasattr(self.player1_game, 'stop'):
            self.player1_game.stop()
        if hasattr(self.player2_game, 'stop'):
            self.player2_game.stop()
        self.destroy()

    def return_to_main_menu(self):
        if messagebox.askyesno("Return to Main Menu", "Are you sure you want to return to the main menu?"):
            self.running = False
            if hasattr(self.player1_game, 'stop'):
                self.player1_game.stop()
            if hasattr(self.player2_game, 'stop'):
                self.player2_game.stop()
                
            self.withdraw()
            
            restart_to_main_menu()

# Player-specific Tetris GUI for the split-screen multiplayer mode
class PlayerTetrisGUI(tk.Frame, Observer):
    def __init__(self, parent, player, is_player1=True):
        tk.Frame.__init__(self, parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.player = player
        self.is_player1 = is_player1
        self.game = None
        
        self.setup_ui()
        
        self.default_cell_size = 25
        self.default_rows = 20
        self.default_cols = 10
    
    def setup_ui(self):
        controls = "W: Rotate, A: Left, S: Down, D: Right, Space: Drop" if self.is_player1 else \
                  "↑: Rotate, ←: Left, ↓: Down, →: Right, Enter: Drop"
        instruction_label = tk.Label(self, text=controls, font=("Arial", 10))
        instruction_label.pack(pady=(0, 10))
        
        self.board_frame = tk.Frame(self, bd=2, relief=tk.SUNKEN)
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        
        self.board_canvas = tk.Canvas(self.board_frame, bg="black", width=250, height=500)
        self.board_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.next_frame = tk.Frame(self)
        self.next_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(self.next_frame, text="Next:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.next_canvas = tk.Canvas(self.next_frame, bg="black", width=80, height=80)
        self.next_canvas.pack(side=tk.LEFT, padx=10)
        
        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.stats_frame, text="Lines:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.lines_var = tk.StringVar(value="0")
        tk.Label(self.stats_frame, textvariable=self.lines_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.stats_frame, text="Level:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
        self.level_var = tk.StringVar(value="1")
        tk.Label(self.stats_frame, textvariable=self.level_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    
    def update(self, subject):
        self.game = subject
        self.update_display()
    
    def update_display(self):
        if not self.game:
            return
            
        data = self.game.get_display_data()
        
        self.lines_var.set(str(data.get('lines', 0)))
        self.level_var.set(str(data.get('level', 1)))
        
        board = data.get('board')
        if not board:
            return
            
        grid = board.plane
        rows, cols = grid.i_length, grid.j_length
        
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 250  
            canvas_height = 500  
            self.board_canvas.update_idletasks()
        
        cell_size = min(canvas_width // cols, canvas_height // rows)
        
        total_grid_width = cell_size * cols
        total_grid_height = cell_size * rows
        start_x = (canvas_width - total_grid_width) // 2
        start_y = (canvas_height - total_grid_height) // 2
        
        self.board_canvas.delete("all")
        
        for i in range(rows):
            for j in range(cols):
                x1 = start_x + j * cell_size
                y1 = start_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                tile = grid.get_tile(i, j)
                if tile:
                    color = tile.color if hasattr(tile, 'color') else "cyan"
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                else:
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
        
        next_piece = data.get('next_piece')
        if next_piece:
            self.next_canvas.delete("all")
            
            preview_cell_size = 15
            
            center_x = 40 - preview_cell_size * 2
            center_y = 40 - preview_cell_size * 2
            
            for tile in next_piece.tiles:
                location = tile.getLocation()
                i, j = location.getI_Location(), location.getJ_Location()
                
                x1 = center_x + (j - next_piece.x_offset) * preview_cell_size
                y1 = center_y + (i - next_piece.y_offset) * preview_cell_size
                x2 = x1 + preview_cell_size
                y2 = y1 + preview_cell_size
                self.next_canvas.create_rectangle(x1, y1, x2, y2, fill=tile.color, outline="black")
        
        self.update_idletasks()
    
    def handle_key(self, key):
        """Handle keyboard input"""
        if self.game and hasattr(self.game, 'handle_input'):
            self.game.handle_input(key)

# Player-specific Candy Crush GUI for the split-screen multiplayer mode
class PlayerCandyCrushGUI(tk.Frame, Observer):
    def __init__(self, parent, player, is_player1=True):
        tk.Frame.__init__(self, parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.player = player
        self.is_player1 = is_player1
        self.game = None
        
        self.game_frame = self
        
        self.time_var = tk.StringVar(value="60")
        self.level_var = tk.StringVar(value="1")
        
        self.candy_colors = {
            "Red": "#FF4444",
            "Orange": "#FF8C00",
            "Yellow": "#FFDD00",
            "Green": "#44FF44",
            "Blue": "#4444FF",
            "Purple": "#9932CC"
        }
        
        self.cursor_i = 0
        self.cursor_j = 0
        self.grid_rows = 9  
        self.grid_cols = 9  
        self.cell_size = 30 
        self.cursor_speed = 1  
        self.key_pressed = False  
        
        for widget in self.winfo_children():
            widget.destroy()
            
        self.setup_candycrush_ui()
        
        self.board_canvas.bind("<Button-1>", self.on_canvas_click)
        
        if self.is_player1:
            self.bind("w", lambda event: self.handle_key("UP"))
            self.bind("a", lambda event: self.handle_key("LEFT"))
            self.bind("s", lambda event: self.handle_key("DOWN"))
            self.bind("d", lambda event: self.handle_key("RIGHT"))
            self.bind("<space>", lambda event: self.handle_key("SPACE"))
        else:
            self.bind("<KeyPress-Up>", lambda event: self.handle_key_press("UP"))
            self.bind("<KeyRelease-Up>", lambda event: self.handle_key_release("UP"))
            
            self.bind("<KeyPress-Down>", lambda event: self.handle_key_press("DOWN"))
            self.bind("<KeyRelease-Down>", lambda event: self.handle_key_release("DOWN"))
            
            self.bind("<KeyPress-Left>", lambda event: self.handle_key_press("LEFT"))
            self.bind("<KeyRelease-Left>", lambda event: self.handle_key_release("LEFT"))
            
            self.bind("<KeyPress-Right>", lambda event: self.handle_key_press("RIGHT"))
            self.bind("<KeyRelease-Right>", lambda event: self.handle_key_release("RIGHT"))
            
            self.bind("<KeyPress-Return>", lambda event: self.handle_key_press("SPACE"))
            self.bind("<KeyRelease-Return>", lambda event: self.handle_key_release("SPACE"))
        
        self.bind("<Tab>", lambda event: self.handle_key("TAB"))
        
        self.focus_set()
        
    def setup_candycrush_ui(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        display_frame = tk.Frame(self.game_frame, bg="#f5f5f5")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        controls_frame = tk.LabelFrame(
            display_frame,
            text="Controls",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        controls_frame.pack(fill=tk.X, padx=10, pady=(10, 15))
        
        if hasattr(self, 'is_player1'):
            if self.is_player1:
                controls_text = "WASD: Move cursor, Space: Select tile"
            else:
                controls_text = "Arrow keys: Move cursor, Enter: Select tile"
        else:
            controls_text = "Arrow keys: Move cursor, Space: Select tile"
        
        controls_label = tk.Label(
            controls_frame, 
            text=controls_text, 
            font=("Arial", 11),
            bg="#f5f5f5",
            fg="#333333"
        )
        controls_label.pack(pady=5)
        
        board_frame = tk.Frame(
            display_frame, 
            bd=3, 
            relief=tk.RIDGE, 
            bg="#6d4c41"  
        )
        board_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15), padx=10)
        
        self.board_canvas = tk.Canvas(
            board_frame, 
            bg="#fff8e1",  
            width=400, 
            height=400, 
            bd=0, 
            highlightthickness=0
        )
        self.board_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        info_frame = tk.Frame(display_frame, bg="#f5f5f5")
        info_frame.pack(fill=tk.X, pady=5, padx=10)
        
        timer_frame = tk.LabelFrame(
            info_frame, 
            text="Time Left", 
            font=("Arial", 11, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        timer_frame.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(
            timer_frame, 
            textvariable=self.time_var, 
            font=("Arial", 14, "bold"), 
            fg="#e53935",  
            bg="#f5f5f5"
        )
        self.time_label.pack(padx=10, pady=5)
        
        level_frame = tk.LabelFrame(
            info_frame, 
            text="Level", 
            font=("Arial", 11, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        level_frame.pack(side=tk.LEFT, padx=20)
        
        level_label = tk.Label(
            level_frame, 
            textvariable=self.level_var, 
            font=("Arial", 14, "bold"),
            fg="#43a047",  
            bg="#f5f5f5"
        )
        level_label.pack(padx=10, pady=5)
        
        instructions_frame = tk.LabelFrame(
            display_frame,
            text="How to Play",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        instructions_frame.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        if hasattr(self, 'is_player1'):
            if self.is_player1:
                instructions_text = """
1. Use WASD keys to move the cursor
2. Press Space to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
            else:
                instructions_text = """
1. Use Arrow keys to move the cursor
2. Press Enter to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
        else:
            instructions_text = """
1. Use Arrow keys to move the cursor
2. Press Space to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
        
        tk.Label(
            instructions_frame, 
            text=instructions_text, 
            justify=tk.LEFT, 
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(padx=10, pady=5)
    
    def update(self, subject):
        self.game = subject
        self.after(100, self.update_display)
    
    def update_display(self):
        if not self.game:
            return
            
        data = self.game.get_display_data()
        
        level = data.get('level', 1)
        self.level_var.set(str(level))
        
        time_left = data.get('time_left', 60)
        if time_left is not None:
            time_str = str(int(time_left))
            self.time_var.set(time_str)
            
            if time_left <= 10:
                self.time_label.config(fg="red", font=("Arial", 10, "bold"))
            elif time_left <= 20:
                self.time_label.config(fg="orange", font=("Arial", 10, "bold"))
            else:
                self.time_label.config(fg="black", font=("Arial", 10, "bold"))
        
        board = data.get('board')
        if not board:
            return
            
        grid = board.plane
        rows, cols = grid.i_length, grid.j_length
        
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300  
            canvas_height = 300  
            self.board_canvas.update_idletasks()
            
        self.cell_size = min(canvas_width // cols, canvas_height // rows)
        
        total_grid_width = self.cell_size * cols
        total_grid_height = self.cell_size * rows
        start_x = (canvas_width - total_grid_width) // 2
        start_y = (canvas_height - total_grid_height) // 2
        
        self.grid_rows = rows
        self.grid_cols = cols
        
        self.board_canvas.delete("all")
        
        for i in range(rows + 1):
            y = start_y + i * self.cell_size
            self.board_canvas.create_line(
                start_x, y, 
                start_x + cols * self.cell_size, y, 
                fill="#CCCCCC"
            )
        
        for j in range(cols + 1):
            x = start_x + j * self.cell_size
            self.board_canvas.create_line(
                x, start_y, 
                x, start_y + rows * self.cell_size, 
                fill="#CCCCCC"
            )
        
        has_tiles = False  
        for i in range(rows):
            for j in range(cols):
                x = start_x + j * self.cell_size
                y = start_y + i * self.cell_size
                
                tile = grid.get_tile(i, j)
                if tile:
                    has_tiles = True  
                    candy_type = tile.candy_type
                    color = self.candy_colors.get(candy_type, "#DDDDDD")
                    
                    if i == self.cursor_i and j == self.cursor_j:
                        self.board_canvas.create_rectangle(
                            x, y, x + self.cell_size, y + self.cell_size,
                            fill="#CCFFCC", outline="#00FF00", width=2
                        )
                    
                    if board.selected_tile and board.selected_tile == tile:
                        self.board_canvas.create_rectangle(
                            x, y, x + self.cell_size, y + self.cell_size,
                            fill="#FFFF00", outline="#FF0000", width=2
                        )
                    
                    size_factor = 0.8  
                    candy_size = self.cell_size * size_factor
                    offset = (self.cell_size - candy_size) / 2
                    
                    self.board_canvas.create_oval(
                        x + offset, y + offset,
                        x + offset + candy_size, y + offset + candy_size,
                        fill=color, outline="black"
                    )
        
        if not has_tiles and self.game:
            print("No tiles found during rendering, attempting to repopulate board")
            if hasattr(self.game, 'board') and hasattr(self.game.board, 'populate_board'):
                self.game.board.populate_board()
                self.after(500, self.update_display)
        
        self.update_idletasks()
    
    def handle_key(self, key):
        if not self.game or not self.game._running:
            return
            
        if key == "UP" and self.cursor_i > 0:
            self.cursor_i -= 1
        elif key == "DOWN" and self.cursor_i < self.grid_rows - 1:
            self.cursor_i += 1
        elif key == "LEFT" and self.cursor_j > 0:
            self.cursor_j -= 1
        elif key == "RIGHT" and self.cursor_j < self.grid_cols - 1:
            self.cursor_j += 1
        elif key == "SPACE":
            self.game.handle_input(self.cursor_i, self.cursor_j)
        elif key == "TAB":
            self.game.handle_input(99, 99)
        
        self.update_display()

    def on_canvas_click(self, event):
        if not self.game or not self.game._running:
            return
            
        if hasattr(self, 'grid_start_x') and hasattr(self, 'grid_start_y'):
            j = (event.x - self.grid_start_x) // self.cell_size
            i = (event.y - self.grid_start_y) // self.cell_size
        else:
            j = event.x // self.cell_size
            i = event.y // self.cell_size
        
        if 0 <= i < self.grid_rows and 0 <= j < self.grid_cols:
            self.cursor_i = i
            self.cursor_j = j
            self.update_display()
            
            self.game.handle_input(i, j)

        """Handle focus event for this frame"""
        print(f"Player {self.player.name}'s candy crush grid focused")

    def handle_key_press(self, key):
        if self.key_pressed:  
            return "break"
            
        self.key_pressed = True
        self.handle_key(key)
        return "break"
        
    def handle_key_release(self, key):
        self.key_pressed = False
        return "break"

# Base class for game GUIs implementing the Observer pattern for game state updates
class TkinterGUI(tk.Tk, Observer):
    def __init__(self, title="Tile Matching Game"):
        super().__init__()
        self.title(title)
        self.state('zoomed')  
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.game = None
        self.running = False
        self.update_rate = 33  
        self.game_over_shown = False  
        
        self.score_var = tk.StringVar(value="0")
        self.level_var = tk.StringVar(value="1")
        
        self.player_frames = []
        self.player_names = []
        self.player_scores = []
        self.player_active = []
        
        self.setup_ui()
        
    def setup_ui(self):
        self.top_bar = tk.Frame(self, bd=1, relief=tk.RAISED, bg="#e0e0e0")
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        
        self.back_button = tk.Button(
            self.top_bar, 
            text="Back to Main Menu", 
            command=self.return_to_main_menu,
            font=("Arial", 10, "bold"),
            bg="#ff9999",
            padx=10,
            pady=3,
            relief=tk.GROOVE
        )
        self.back_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        game_title = tk.Label(
            self.top_bar, 
            text=self.title(), 
            font=("Arial", 14, "bold"),
            bg="#e0e0e0"
        )
        game_title.pack(side=tk.LEFT, padx=20, pady=5)
        
        self.main_frame = tk.Frame(self, bg="#f5f5f5")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.top_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.top_frame.pack(fill=tk.X)
        
        self.info_frame = tk.Frame(self.top_frame, bg="#f5f5f5", padx=5, pady=5)
        self.info_frame.pack(side=tk.LEFT)
        
        tk.Label(self.info_frame, text="Score:", font=("Arial", 12, "bold"), bg="#f5f5f5").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.info_frame, textvariable=self.score_var, font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#1e88e5").grid(row=0, column=1, padx=5)
        
        tk.Label(self.info_frame, text="Level:", font=("Arial", 12, "bold"), bg="#f5f5f5").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self.info_frame, textvariable=self.level_var, font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#1e88e5").grid(row=1, column=1, padx=5)
        
        self.control_frame = tk.Frame(self.top_frame, bg="#f5f5f5")
        self.control_frame.pack(side=tk.RIGHT)
        
        self.pause_button = tk.Button(
            self.control_frame, 
            text="Pause", 
            command=self.toggle_pause,
            font=("Arial", 10, "bold"),
            bg="#42a5f5",
            fg="white",
            padx=10,
            pady=3,
            relief=tk.GROOVE
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.restart_button = tk.Button(
            self.control_frame, 
            text="Restart", 
            command=self.restart_game,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=3,
            relief=tk.GROOVE
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        self.switch_button = tk.Button(
            self.control_frame, 
            text="Switch Player", 
            command=self.switch_player,
            font=("Arial", 10, "bold"),
            bg="#ff9800",
            fg="white",
            padx=10,
            pady=3,
            relief=tk.GROOVE
        )
        self.switch_button.pack(side=tk.LEFT, padx=5)
        
        self.players_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.players_label = tk.Label(self.players_frame, text="Players:", font=("Arial", 12, "bold"), bg="#f5f5f5")
        self.players_label.pack(side=tk.LEFT, padx=(0, 10))

        self.game_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.game_frame.pack(fill=tk.BOTH, expand=True)
    
    def return_to_main_menu(self):
        if messagebox.askyesno("Return to Main Menu", "Are you sure you want to return to the main menu?"):
            self.running = False
            if self.game:
                self.game.stop()
                
            self.withdraw()
            
            restart_to_main_menu()
    
    def update_players_display(self, players_data):
        if not players_data:
            if hasattr(self, 'players_frame') and self.players_frame.winfo_exists():
                self.players_frame.pack_forget()
            return
        else:
            if not hasattr(self, 'players_frame') or not self.players_frame.winfo_exists():
                self.players_frame = tk.Frame(self.main_frame)
                self.players_label = tk.Label(self.players_frame, text="Players:", font=("Arial", 12, "bold"), bg="#f5f5f5")
                self.players_label.pack(side=tk.LEFT, padx=(0, 10))
            
            self.players_frame.pack(fill=tk.X, pady=10)
            
        if len(self.player_frames) != len(players_data):
            for widget in self.players_frame.winfo_children():
                if widget != self.players_label:  
                    widget.destroy()
            
            self.player_frames = []
            self.player_names = []
            self.player_scores = []
            self.player_active = []
            
            for idx, player_data in enumerate(players_data):
                player_frame = tk.Frame(self.players_frame, bd=2)
                player_frame.pack(side=tk.LEFT, padx=10, pady=5)
                
                name_var = tk.StringVar(value=player_data.get('name', f'Player {idx+1}'))
                name_label = tk.Label(player_frame, textvariable=name_var, font=("Arial", 11))
                name_label.pack(side=tk.LEFT, padx=5)
                
                score_var = tk.StringVar(value=f"Score: {player_data.get('score', 0)}")
                score_label = tk.Label(player_frame, textvariable=score_var, font=("Arial", 11))
                score_label.pack(side=tk.LEFT, padx=5)
                
                active_var = tk.BooleanVar(value=player_data.get('is_active', False))
                active_label = tk.Label(player_frame, text="Active", font=("Arial", 9), fg="blue")
                if active_var.get():
                    active_label.pack(side=tk.LEFT, padx=5)
                    player_frame.config(bg="#E0E0FF", relief=tk.GROOVE)
                else:
                    player_frame.config(bg=self.cget('bg'), relief=tk.FLAT)
                
                self.player_frames.append(player_frame)
                self.player_names.append(name_var)
                self.player_scores.append(score_var)
                self.player_active.append((active_var, active_label))
        else:
            for idx, player_data in enumerate(players_data):
                frame = self.player_frames[idx]
                self.player_names[idx].set(player_data.get('name', f'Player {idx+1}'))
                self.player_scores[idx].set(f"Score: {player_data.get('score', 0)}")
                
                active_var, active_label = self.player_active[idx]
                new_active = player_data.get('is_active', False)
                
                if new_active != active_var.get():
                    active_var.set(new_active)
                    if new_active:
                        active_label.pack(side=tk.LEFT, padx=5)
                        frame.config(bg="#E0E0FF", relief=tk.GROOVE)
                    else:
                        active_label.pack_forget()
                        frame.config(bg=self.cget('bg'), relief=tk.FLAT)
    
    def update(self, subject):
        self.game = subject
        self.update_display()
    
    def update_display(self):
        if not self.game:
            return
            
        data = self.game.get_display_data()
        
        self.score_var.set(str(data.get('score', 0)))
        self.level_var.set(str(data.get('level', 1)))
        
        self.update_players_display(data.get('players', []))
        
        self.update_game_display(data)
    
    def update_game_display(self, data):
        pass
    
    def toggle_pause(self):
        if not self.game:
            return
            
        if self.game._running:
            self.game.pause()
            self.pause_button.config(text="Resume")
        else:
            self.game.start()
            self.pause_button.config(text="Pause")
    
    def restart_game(self):
        """Restart the game"""
        if not self.game:
            return
            
        self.game_over_shown = False
        
        if hasattr(self.game, 'stop'):
            self.game.stop()
        
        game_type = self.game.__class__
        self.game = game_type()
        
        self.game.register_observer(self)
        
        if hasattr(self.game, 'players'):
            for player in self.game.players:
                player.update_score(-player.score)  
        
        self.game.start()
        self.pause_button.config(text="Pause")
        
        self.restart_button.config(bg="SystemButtonFace", fg="black", font=("Arial", 10))
    
    def switch_player(self):
        """Switch to the next player"""
        if not self.game or not hasattr(self.game, 'switch_player'):
            return
            
        game_name = self.game.__class__.__name__
        
        if game_name == "Tetris":
            self.handle_key("TAB")
        elif game_name == "CandyCrush":
            self.game.handle_input(99, 99)
            
        self.update_display()
    
    def start_game_loop(self):
        """Start the main game update loop"""
        self.running = True
        self.update_game()
    
    def update_game(self):
        """Main game loop"""
        if not self.running:
            return
            
        if self.game and hasattr(self.game, 'update'):
            self.game.update()
        
        if hasattr(self.game, 'game_over') and self.game.game_over and not self.game_over_shown:
            self.game_over_shown = True
            
            player_data = []
            data = self.game.get_display_data()
            players = data.get('players', [])
            
            if players:
                high_score = -1
                winner = None
                
                for player in players:
                    score = player.get('score', 0)
                    player_data.append(f"{player.get('name', 'Player')}: {score}")
                    
                    if score > high_score:
                        high_score = score
                        winner = player.get('name', 'Player')
                
                msg = f"Game Over!\n\n" + "\n".join(player_data)
                
                if len(players) > 1 and winner:
                    msg += f"\n\nWinner: {winner}!"
            else:
                msg = f"Game Over!\n\nFinal Score: {data.get('score', 0)}"
            
            self.after(100, lambda: messagebox.showinfo("Game Over", msg))
            
            self.restart_button.config(bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        
        self.after(self.update_rate, self.update_game)
    
    def on_close(self):
        """Handle window close event"""
        self.running = False
        if self.game:
            self.game.stop()
        self.destroy()

# Tetris specific implementation of the game GUI 
class TetrisGUI(TkinterGUI):
    def __init__(self):
        super().__init__("Tetris")
        
        self.setup_tetris_ui()
        
        self.bind("<Left>", lambda event: self.handle_key("LEFT"))
        self.bind("<Right>", lambda event: self.handle_key("RIGHT"))
        self.bind("<Down>", lambda event: self.handle_key("DOWN"))
        self.bind("<Up>", lambda event: self.handle_key("UP"))
        self.bind("<space>", lambda event: self.handle_key("SPACE"))
        self.bind("<Tab>", lambda event: self.handle_key("TAB"))
        
    def setup_tetris_ui(self):
        """Set up Tetris-specific UI components with improved styling"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.display_frame = tk.Frame(self.game_frame, bg="#f5f5f5")
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.board_frame = tk.Frame(self.display_frame, bd=3, relief=tk.RIDGE, bg="#333333")
        self.board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.board_canvas = tk.Canvas(self.board_frame, bg="#000000", bd=0, highlightthickness=0)
        self.board_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.info_frame = tk.Frame(self.display_frame, width=200, bg="#f5f5f5", relief=tk.GROOVE, bd=2)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        self.info_frame.pack_propagate(False)  
        
        next_title = tk.Label(
            self.info_frame, 
            text="Next Piece", 
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        next_title.pack(pady=(10, 5))
        
        next_frame = tk.Frame(self.info_frame, bg="#333333", bd=2, relief=tk.SUNKEN, padx=2, pady=2)
        next_frame.pack(pady=(0, 20))
        
        self.next_piece_canvas = tk.Canvas(next_frame, bg="#000000", width=150, height=150, bd=0, highlightthickness=0)
        self.next_piece_canvas.pack(padx=2, pady=2)
        
        stats_frame = tk.LabelFrame(
            self.info_frame, 
            text="Statistics", 
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        stats_frame.pack(fill=tk.X, pady=10, padx=5)
        
        lines_frame = tk.Frame(stats_frame, bg="#f5f5f5")
        lines_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(lines_frame, text="Lines:", font=("Arial", 11, "bold"), bg="#f5f5f5").pack(side=tk.LEFT)
        self.lines_var = tk.StringVar(value="0")
        tk.Label(lines_frame, textvariable=self.lines_var, font=("Arial", 11, "bold"), fg="#1e88e5", bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
        
        instruction_frame = tk.LabelFrame(
            self.info_frame,
            text="Controls",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        instruction_frame.pack(fill=tk.X, pady=10, padx=5)
        
        instruction_text = """
← / →    : Move left/right
↑         : Rotate piece
↓         : Move down
Space : Hard drop
Tab     : Switch player
        """
        tk.Label(
            instruction_frame, 
            text=instruction_text, 
            justify=tk.LEFT, 
            font=("Consolas", 10),
            bg="#f5f5f5"
        ).pack(pady=5)
    
    def update_game_display(self, data):
        """Update the Tetris game display"""
        self.lines_var.set(str(data.get('lines', 0)))
        
        board = data.get('board')
        if not board:
            return
            
        grid = board.plane
        rows, cols = grid.i_length, grid.j_length
        
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.board_canvas.update_idletasks()
            return
        
        cell_size = min(canvas_width // cols, canvas_height // rows)
        
        total_grid_width = cell_size * cols
        total_grid_height = cell_size * rows
        start_x = (canvas_width - total_grid_width) // 2
        start_y = (canvas_height - total_grid_height) // 2
        
        self.board_canvas.delete("all")
        
        for i in range(rows):
            for j in range(cols):
                x1 = start_x + j * cell_size
                y1 = start_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                
                tile = grid.get_tile(i, j)
                if tile:
                    if hasattr(tile, 'color'):
                        color = tile.color
                    else:
                        color = "cyan"      
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                else:
                    self.board_canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
        
        next_piece = data.get('next_piece')
        if next_piece:
            self.next_piece_canvas.delete("all")
            
            preview_width = self.next_piece_canvas.winfo_width()
            preview_height = self.next_piece_canvas.winfo_height()
            preview_cell_size = min(preview_width, preview_height) // 6
            
            center_x = preview_width // 2 - preview_cell_size * 2
            center_y = preview_height // 2 - preview_cell_size * 2
            
            for tile in next_piece.tiles:
                location = tile.getLocation()
                i, j = location.getI_Location(), location.getJ_Location()
                x1 = center_x + (j - next_piece.x_offset) * preview_cell_size
                y1 = center_y + (i - next_piece.y_offset) * preview_cell_size
                x2 = x1 + preview_cell_size
                y2 = y1 + preview_cell_size
                self.next_piece_canvas.create_rectangle(x1, y1, x2, y2, fill=tile.color, outline="black")
    
    def handle_key(self, key):
        """Handle keyboard input for Tetris game"""
        if self.game and self.game._running:
            self.game.handle_input(key)

# Candy Crush-specific implementation of the game GUI with themed visuals
class CandyCrushGUI(TkinterGUI):
    def __init__(self):
        super().__init__("Candy Crush")
        
        self.time_var = tk.StringVar(value="60")
        self.level_var = tk.StringVar(value="1")
        
        self.candy_colors = {
            "Red": "#FF4444",
            "Orange": "#FF8C00",
            "Yellow": "#FFDD00",
            "Green": "#44FF44",
            "Blue": "#4444FF",
            "Purple": "#9932CC"
        }
        
        self.is_player1 = True
        
        self.player = type('obj', (object,), {'name': 'Player 1'})
        
        self.cursor_i = 0
        self.cursor_j = 0
        self.grid_rows = 9  
        self.grid_cols = 9  
        self.cell_size = 30 
        
        self.setup_candycrush_ui()
        
        self.board_canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.bind("<Up>", lambda event: self.handle_key("UP"))
        self.bind("<Down>", lambda event: self.handle_key("DOWN"))
        self.bind("<Left>", lambda event: self.handle_key("LEFT"))
        self.bind("<Right>", lambda event: self.handle_key("RIGHT"))
        self.bind("<space>", lambda event: self.handle_key("SPACE"))
        self.bind("<Tab>", lambda event: self.handle_key("TAB"))
        
        self.focus_set()
    
    def setup_candycrush_ui(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        display_frame = tk.Frame(self.game_frame, bg="#f5f5f5")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        controls_frame = tk.LabelFrame(
            display_frame,
            text="Controls",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        controls_frame.pack(fill=tk.X, padx=10, pady=(10, 15))
        
        if hasattr(self, 'is_player1'):
            if self.is_player1:
                controls_text = "WASD: Move cursor, Space: Select tile"
            else:
                controls_text = "Arrow keys: Move cursor, Enter: Select tile"
        else:
            controls_text = "Arrow keys: Move cursor, Space: Select tile"
        
        controls_label = tk.Label(
            controls_frame, 
            text=controls_text, 
            font=("Arial", 11),
            bg="#f5f5f5",
            fg="#333333"
        )
        controls_label.pack(pady=5)
        
        board_frame = tk.Frame(
            display_frame, 
            bd=3, 
            relief=tk.RIDGE, 
            bg="#6d4c41"  
        )
        board_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15), padx=10)
        
        self.board_canvas = tk.Canvas(
            board_frame, 
            bg="#fff8e1",  
            width=400, 
            height=400, 
            bd=0, 
            highlightthickness=0
        )
        self.board_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        info_frame = tk.Frame(display_frame, bg="#f5f5f5")
        info_frame.pack(fill=tk.X, pady=5, padx=10)
        
        timer_frame = tk.LabelFrame(
            info_frame, 
            text="Time Left", 
            font=("Arial", 11, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        timer_frame.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(
            timer_frame, 
            textvariable=self.time_var, 
            font=("Arial", 14, "bold"), 
            fg="#e53935",  
            bg="#f5f5f5"
        )
        self.time_label.pack(padx=10, pady=5)
        
        level_frame = tk.LabelFrame(
            info_frame, 
            text="Level", 
            font=("Arial", 11, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        level_frame.pack(side=tk.LEFT, padx=20)
        
        level_label = tk.Label(
            level_frame, 
            textvariable=self.level_var, 
            font=("Arial", 14, "bold"),
            fg="#43a047",  
            bg="#f5f5f5"
        )
        level_label.pack(padx=10, pady=5)
        
        instructions_frame = tk.LabelFrame(
            display_frame,
            text="How to Play",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            bd=2,
            relief=tk.GROOVE,
            padx=10,
            pady=5
        )
        instructions_frame.pack(fill=tk.X, pady=(5, 10), padx=10)
        
        if hasattr(self, 'is_player1'):
            if self.is_player1:
                instructions_text = """
1. Use WASD keys to move the cursor
2. Press Space to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
            else:
                instructions_text = """
1. Use Arrow keys to move the cursor
2. Press Enter to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
        else:
            instructions_text = """
1. Use Arrow keys to move the cursor
2. Press Space to select a candy
3. Select an adjacent candy to swap
4. Match 3+ candies in a row or column
                """
        
        tk.Label(
            instructions_frame, 
            text=instructions_text, 
            justify=tk.LEFT, 
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(padx=10, pady=5)
    
    def update_game_display(self, data):
        if not self.game:
            return
        
        self.board = data.get('board')
        self.score = data.get('score', 0)
        self.level = data.get('level', 1)
        self.players_data = data.get('players', [])
        
        self.score_var.set(str(self.score))
        
        time_left = data.get('time_left', 60)  
        if time_left is not None:
            time_str = str(int(time_left))
            self.time_var.set(time_str)
            
            if time_left <= 10:
                self.time_label.config(fg="red", font=("Arial", 16, "bold"))
            elif time_left <= 20:
                self.time_label.config(fg="orange", font=("Arial", 16, "bold"))
            else:
                self.time_label.config(fg="black", font=("Arial", 16, "bold"))
        
        if not hasattr(self, 'cursor_i'):
            self.cursor_i = 0
            self.cursor_j = 0
        
        if self.players_data:
            self.update_players_display(self.players_data)
        
        if self.board and hasattr(self.board, 'plane'):
            grid = self.board.plane
            self.grid_rows = grid.i_length
            self.grid_cols = grid.j_length
        else:
            self.grid_rows = 9
            self.grid_cols = 9
        
        self.cursor_i = min(max(0, self.cursor_i), self.grid_rows - 1)
        self.cursor_j = min(max(0, self.cursor_j), self.grid_cols - 1)
        
        self.update_candy_display()
    
    def update_candy_display(self):
        if not self.board or not hasattr(self.board, 'plane'):
            return
            
        self.board_canvas.delete("all")
        
        canvas_width = self.board_canvas.winfo_width()
        canvas_height = self.board_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 300
        
        cell_size = min(canvas_width // self.grid_cols, canvas_height // self.grid_rows)
        
        start_x = (canvas_width - (cell_size * self.grid_cols)) // 2
        start_y = (canvas_height - (cell_size * self.grid_rows)) // 2
        
        for i in range(self.grid_rows):
            for j in range(self.grid_cols):
                x = start_x + (j * cell_size)
                y = start_y + (i * cell_size)
                
                if i == self.cursor_i and j == self.cursor_j:
                    self.board_canvas.create_rectangle(
                        x, y, x + cell_size, y + cell_size,
                        fill="#F8F8F8", outline="red", width=3
                    )
                elif hasattr(self.board, 'selected_tile') and self.board.selected_tile:
                    selected_loc = self.board.selected_tile.getLocation()
                    selected_i, selected_j = selected_loc.getI_Location(), selected_loc.getJ_Location()
                    
                    if i == selected_i and j == selected_j:
                        self.board_canvas.create_rectangle(
                            x, y, x + cell_size, y + cell_size,
                            fill="#F8F8F8", outline="blue", width=3
                        )
                    else:
                        self.board_canvas.create_rectangle(
                            x, y, x + cell_size, y + cell_size,
                            fill="#F8F8F8", outline="gray"
                        )
                else:
                    self.board_canvas.create_rectangle(
                        x, y, x + cell_size, y + cell_size,
                        fill="#F8F8F8", outline="gray"
                    )
                
                tile = self.board.plane.get_tile(i, j)
                if tile and hasattr(tile, 'candy_type'):
                    color = self.candy_colors.get(tile.candy_type, "gray")
                    
                    size_factor = 0.8  
                    candy_size = cell_size * size_factor
                    offset = (cell_size - candy_size) / 2
                    
                    self.board_canvas.create_oval(
                        x + offset, y + offset,
                        x + offset + candy_size, y + offset + candy_size,
                        fill=color, outline="black"
                    )
        
        self.update_idletasks()
    
    def handle_key(self, key):
        if not self.game or not self.game._running:
            return
            
        if key == "UP" and self.cursor_i > 0:
            self.cursor_i -= 1
        elif key == "DOWN" and self.cursor_i < self.grid_rows - 1:
            self.cursor_i += 1
        elif key == "LEFT" and self.cursor_j > 0:
            self.cursor_j -= 1
        elif key == "RIGHT" and self.cursor_j < self.grid_cols - 1:
            self.cursor_j += 1
        elif key == "SPACE":
            self.game.handle_input(self.cursor_i, self.cursor_j)
        elif key == "TAB":
            self.game.handle_input(99, 99)
        
        self.update_display()
        
    def on_canvas_click(self, event):
        if not self.game or not self.game._running:
            return
            
        if hasattr(self, 'grid_start_x') and hasattr(self, 'grid_start_y'):
            j = (event.x - self.grid_start_x) // self.cell_size
            i = (event.y - self.grid_start_y) // self.cell_size
        else:
            j = event.x // self.cell_size
            i = event.y // self.cell_size
        
        if 0 <= i < self.grid_rows and 0 <= j < self.grid_cols:
            self.cursor_i = i
            self.cursor_j = j
            self.update_display()
            
            self.game.handle_input(i, j)

    def on_focus(self, event):
        print(f"Player {self.player.name}'s candy crush grid focused") 