from tmge import Menu, Player
from tetris import Tetris
from candycrush import CandyCrush
from gui_tkinter import TetrisGUI, CandyCrushGUI, SplitScreenMultiplayerGUI
import tkinter as tk
from tkinter import ttk

def main():
    # Initialize game menu and register available games
    menu = Menu()
    menu.register_game(Tetris)
    menu.register_game(CandyCrush)

    # Setup main window and styling
    root = tk.Tk()
    root.title("Tile Matching Game Environment")
    root.state('zoomed')
    root.resizable(True, True)
    root.configure(bg="#f0f0f5")
    
    main_container = tk.Frame(root, bg="#f0f0f5", padx=30, pady=20)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    header_frame = tk.Frame(main_container, bg="#6a5acd")
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = tk.Label(
        header_frame, 
        text="Tile Matching Game Environment", 
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#6a5acd",
        padx=15,
        pady=15
    )
    title_label.pack()
    
    content_frame = tk.Frame(main_container, bg="#f0f0f5")
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Game selection area
    left_frame = tk.Frame(content_frame, bg="#f0f0f5")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    # Setup game selection interface
    game_select_frame = tk.LabelFrame(
        left_frame, 
        text="Select Game", 
        font=("Arial", 14, "bold"),
        bg="#f8f8ff",
        fg="#483d8b",
        padx=15,
        pady=15,
        relief=tk.GROOVE,
        bd=2
    )
    game_select_frame.pack(fill=tk.BOTH, expand=True)
    
    selected_game = tk.IntVar(value=0)
    
    game_icons = {
        "Tetris": "■ ■ ■ ■",  
        "CandyCrush": "● ● ●" 
    }
    
    game_descriptions = {
        "Tetris": "Classic block-stacking puzzle game.",
        "CandyCrush": "Match and swap colorful candies."
    }
    
    # Create game options
    for idx, game_cls in enumerate(menu.available_games):
        game_name = game_cls.__name__
        
        game_option = tk.Frame(game_select_frame, bg="#f8f8ff", pady=5)
        game_option.pack(fill=tk.X, pady=8)
        
        radio = tk.Radiobutton(
            game_option, 
            text=game_name, 
            variable=selected_game, 
            value=idx,
            font=("Arial", 12, "bold"),
            bg="#f8f8ff",
            activebackground="#e6e6fa"
        )
        radio.pack(anchor=tk.W)
        
        icon_label = tk.Label(
            game_option, 
            text=game_icons.get(game_name, ""),
            font=("Arial", 14, "bold"),
            fg="#6a5acd",
            bg="#f8f8ff"
        )
        icon_label.pack(anchor=tk.W, padx=(20, 0), pady=(5, 0))
        
        desc_label = tk.Label(
            game_option, 
            text=game_descriptions.get(game_name, ""),
            font=("Arial", 9),
            fg="#555555",
            bg="#f8f8ff",
            wraplength=250,
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, padx=(20, 0), pady=(5, 10))
    
    # Player settings area
    right_frame = tk.Frame(content_frame, bg="#f0f0f5")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    # Configure player settings and controls
    player_frame = tk.LabelFrame(
        right_frame, 
        text="Player Settings", 
        font=("Arial", 14, "bold"),
        bg="#f8f8ff",
        fg="#483d8b",  
        padx=15,
        pady=15,
        relief=tk.GROOVE,
        bd=2
    )
    player_frame.pack(fill=tk.BOTH, expand=True)
    
    num_players_frame = tk.Frame(player_frame, bg="#f8f8ff")
    num_players_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(
        num_players_frame, 
        text="Number of Players:", 
        font=("Arial", 12, "bold"),
        bg="#f8f8ff"
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    num_players_var = tk.IntVar(value=1)
    
    player_option_style = {
        "font": ("Arial", 11),
        "bg": "#f8f8ff",
        "activebackground": "#e6e6fa"
    }
    
    rb_1player = tk.Radiobutton(
        num_players_frame, 
        text="1 Player", 
        variable=num_players_var, 
        value=1, 
        command=lambda: update_player_fields(),
        **player_option_style
    )
    rb_1player.pack(side=tk.LEFT, padx=10)
    
    rb_2player = tk.Radiobutton(
        num_players_frame, 
        text="2 Players", 
        variable=num_players_var, 
        value=2, 
        command=lambda: update_player_fields(),
        **player_option_style
    )
    rb_2player.pack(side=tk.LEFT, padx=10)
    
    separator = ttk.Separator(player_frame, orient='horizontal')
    separator.pack(fill=tk.X, pady=10)
    
    players_container = tk.Frame(player_frame, bg="#f8f8ff")
    players_container.pack(fill=tk.X, pady=5)
    
    player1_frame = tk.Frame(players_container, bg="#f8f8ff")
    player1_frame.pack(fill=tk.X, pady=5)
    
    tk.Label(
        player1_frame, 
        text="Player 1:", 
        font=("Arial", 12),
        bg="#f8f8ff"
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    player1_entry = tk.Entry(
        player1_frame, 
        font=("Arial", 12),
        bd=2,
        relief=tk.GROOVE
    )
    player1_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    player1_entry.insert(0, "Player 1")
    
    player2_frame = tk.Frame(players_container, bg="#f8f8ff")
    
    tk.Label(
        player2_frame, 
        text="Player 2:", 
        font=("Arial", 12),
        bg="#f8f8ff"
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    player2_entry = tk.Entry(
        player2_frame, 
        font=("Arial", 12),
        bd=2,
        relief=tk.GROOVE
    )
    player2_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    player2_entry.insert(0, "Player 2")
    
    help_frame = tk.LabelFrame(
        player_frame,
        text="Controls",
        font=("Arial", 12, "bold"),
        bg="#f8f8ff",
        fg="#483d8b",
        bd=2,
        relief=tk.GROOVE
    )
    help_frame.pack(fill=tk.X, pady=(15, 5))
    
    help_text = "Single-player mode: Use arrow keys to control the game."
    help_label = tk.Label(
        help_frame, 
        text=help_text, 
        font=("Arial", 10),
        bg="#f8f8ff",
        justify=tk.LEFT,
        padx=10,
        pady=10
    )
    help_label.pack(fill=tk.X)
    
    button_container = tk.Frame(main_container, bg="#f0f0f5", pady=15)
    button_container.pack(fill=tk.X)
    
    buttons_row = tk.Frame(button_container, bg="#f0f0f5")
    buttons_row.pack(pady=10)
    
    def exit_application():
        root.destroy()
    
    def update_player_fields():
        # Updates UI based on number of players selected
        if num_players_var.get() > 1:
            player2_frame.pack(fill=tk.X, pady=5)
            help_label.config(text="Two-player mode: Each player has their own game screen.\nPlayer 1 uses WASD keys, Player 2 uses arrow keys.")
            print("Player 2 frame shown")
        else:
            player2_frame.pack_forget()
            help_label.config(text="Single-player mode: Use arrow keys to control the game.")
            print("Player 2 frame hidden")
        
        root.update_idletasks()
    
    def start_game():
        # Initializes and starts the selected game with player configuration
        game_idx = selected_game.get()
        chosen_game_class = menu.available_games[game_idx]
        
        player1_name = player1_entry.get() if player1_entry else "Player 1"
        
        player2_name = "Player 2"  
        if num_players_var.get() > 1 and player2_frame.winfo_ismapped():
            try:
                player2_name = player2_entry.get() or "Player 2"
            except Exception as e:
                print(f"Error getting player 2 name: {e}")
                player2_name = "Player 2"
                
        player1 = Player(player1_name)
        player2 = Player(player2_name)
        
        root.destroy()
        
        if num_players_var.get() > 1:
            multi_gui = SplitScreenMultiplayerGUI(chosen_game_class, player1, player2)
            multi_gui.start_game_loop()
            multi_gui.mainloop()
        else:
            if chosen_game_class == Tetris:
                gui = TetrisGUI()
            else:  
                gui = CandyCrushGUI()
            
            game = menu.new_game(chosen_game_class)
            game.add_player(player1)
            game.register_observer(gui)
            game.start()
            
            gui.start_game_loop()
            gui.mainloop()
    
    start_button = tk.Button(
        buttons_row, 
        text="Start Game", 
        command=start_game,
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=25,
        pady=10,
        relief=tk.RAISED,
        bd=3,
        activebackground="#45a049"
    )
    start_button.pack(side=tk.LEFT, padx=10)
    
    exit_button = tk.Button(
        buttons_row,
        text="Exit",
        command=exit_application,
        font=("Arial", 14, "bold"),
        bg="#f44336",
        fg="white",
        padx=25,
        pady=10,
        relief=tk.RAISED,
        bd=3,
        activebackground="#d32f2f"
    )
    exit_button.pack(side=tk.LEFT, padx=10)
    
    update_player_fields()
    
    root.mainloop()

if __name__ == "__main__":
    main()
