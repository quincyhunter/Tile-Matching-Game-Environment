from tmge import Game, GameBoard, Tile, Location
from observer import Subject
import random

# Defines all tetris pieces and their rotations
pieces = {
    'I': [
        [(0,0), (0,1), (0,2), (0,3)],
        [(0,0), (1,0), (2,0), (3,0)]
    ],
    'J': [
        [(0,0), (1,0), (1,1), (1,2)],
        [(0,0), (0,1), (1,0), (2,0)],
        [(0,0), (0,1), (0,2), (1,2)],
        [(0,1), (1,1), (2,0), (2,1)]
    ],
    'L': [
        [(0,2), (1,0), (1,1), (1,2)],
        [(0,0), (1,0), (2,0), (2,1)],
        [(0,0), (0,1), (0,2), (1,0)],
        [(0,0), (0,1), (1,1), (2,1)]
    ],
    'O': [
        [(0,0), (0,1), (1,0), (1,1)]
    ],
    'S': [
        [(0,1), (0,2), (1,0), (1,1)],
        [(0,0), (1,0), (1,1), (2,1)]
    ],
    'T': [
        [(0,1), (1,0), (1,1), (1,2)],
        [(0,0), (1,0), (1,1), (2,0)],
        [(0,0), (0,1), (0,2), (1,1)],
        [(0,1), (1,0), (1,1), (2,1)]
    ],
    'Z': [
        [(0,0), (0,1), (1,1), (1,2)],
        [(0,1), (1,0), (1,1), (2,0)]
    ]
}

class TetrisTile(Tile):
    def __init__(self, location=None, color="cyan"):
        super().__init__(location, 100) 
        self.color = color
        
    def __str__(self):
        return "[]"

class TetrisPiece:
    # Represents a tetris piece with position rotation and color
    def __init__(self, shape, x_offset=3, y_offset=0):
        self.shape = shape
        self.rotation = 0
        self.tiles = []
        self.x_offset = x_offset
        self.y_offset = y_offset
        
        colors = {
            'I': 'cyan', 'J': 'blue', 'L': 'orange',
            'O': 'yellow', 'S': 'green', 'T': 'purple', 'Z': 'red'
        }
        
        for x, y in pieces[shape][self.rotation]:
            loc = Location(y + y_offset, x + x_offset)
            tile = TetrisTile(loc, colors[shape])
            self.tiles.append(tile)
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(pieces[self.shape])
        for idx, (x, y) in enumerate(pieces[self.shape][self.rotation]):
            location = self.tiles[idx].getLocation()
            location.setI_Location(y + self.y_offset)
            location.setJ_Location(x + self.x_offset)
    
    def move(self, di, dj):
        self.y_offset += di
        self.x_offset += dj
        
        for tile in self.tiles:
            location = tile.getLocation()
            location.setI_Location(location.getI_Location() + di)
            location.setJ_Location(location.getJ_Location() + dj)

class TetrisBoard(GameBoard):
    # Manages the game board state, piece movement and collision detection
    def __init__(self, rows: int = 20, cols: int = 10):
        super().__init__(rows, cols)
        self.current_piece = None
        self.next_piece = None
        self.generate_next_piece()
        
    def generate_next_piece(self):
        shapes = list(pieces.keys())
        return TetrisPiece(random.choice(shapes))
    
    def spawn_piece(self):
        if self.current_piece:
            self.current_piece = None
        
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = self.generate_next_piece()
        
        self.next_piece = self.generate_next_piece()
        
        print(f"Spawning piece: {self.current_piece.shape}")
        
        # Check game over condition
        if not self.is_valid_position(self.current_piece):
            print("Cannot place piece at starting position - game over condition")
            return False
        
        self.place_piece()
        return True
        
    def place_piece(self):
        for tile in self.current_piece.tiles:
            location = tile.getLocation()
            i, j = location.getI_Location(), location.getJ_Location()
            self.plane.set_tile(i, j, tile)
    
    def remove_piece(self):
        if self.current_piece:
            for tile in self.current_piece.tiles:
                location = tile.getLocation()
                i, j = location.getI_Location(), location.getJ_Location()
                self.plane.clear_tile(i, j)
    
    # Checks if a piece's position is valid 
    def is_valid_position(self, piece):
        for tile in piece.tiles:
            location = tile.getLocation()
            i, j = location.getI_Location(), location.getJ_Location()
            
            if (i < 0 or i >= self.plane.i_length or
                j < 0 or j >= self.plane.j_length):
                return False
                
            existing_tile = self.plane.get_tile(i, j)
            if existing_tile and existing_tile not in piece.tiles:
                return False
        return True
    
    def move_piece(self, di, dj):
        if not self.current_piece:
            return False
            
        self.remove_piece()
        self.current_piece.move(di, dj)
        
        if self.is_valid_position(self.current_piece):
            self.place_piece()
            return True
        else:
            self.current_piece.move(-di, -dj)
            self.place_piece()
            return False
    
    def rotate_piece(self):
        if not self.current_piece:
            return False
            
        self.remove_piece()
        original_rotation = self.current_piece.rotation
        self.current_piece.rotate()
        
        if self.is_valid_position(self.current_piece):
            self.place_piece()
            return True
        else:
            self.current_piece.rotation = original_rotation
            for idx, (x, y) in enumerate(pieces[self.current_piece.shape][self.current_piece.rotation]):
                location = self.current_piece.tiles[idx].getLocation()
                location.setI_Location(y + self.current_piece.y_offset)
                location.setJ_Location(x + self.current_piece.x_offset)
            self.place_piece()
            return False
    
    # Handles line clearing and updates the board state
    def clear_full_lines(self):
        lines_cleared = 0
        grid = self.plane
        
        for i in range(grid.i_length):
            is_full = True
            for j in range(grid.j_length):
                if not grid.get_tile(i, j):
                    is_full = False
                    break
            
            if is_full:
                lines_cleared += 1
                for row in range(i, 0, -1):
                    for col in range(grid.j_length):
                        above_tile = grid.get_tile(row-1, col)
                        grid.set_tile(row, col, above_tile)
                
                for col in range(grid.j_length):
                    grid.clear_tile(0, col)
        
        return lines_cleared
    
    def lock_piece(self):
        if not self.current_piece:
            return 0
            
        lines_cleared = self.clear_full_lines()
        self.current_piece = None
        return lines_cleared

class Tetris(Game):
    # Main game logic controller handling scoring levels and flow
    def __init__(self):
        super().__init__()
        self.board = TetrisBoard()
        self._running = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.players = []
        self.move_timer = 0
        self.move_delay = 1.0  
        self.game_over = False
        self.active_player_index = 0
        
    def add_player(self, player):
        self.players.append(player)
        
    def start(self):
        self._running = True
        self.timer.start()
        self.move_timer = 0
        
        if not self.board.next_piece:
            self.board.next_piece = self.board.generate_next_piece()
        
        if not self.board.current_piece:
            print("Spawning initial piece")
            success = self.board.spawn_piece()
            if not success:
                print("Failed to place initial piece, creating new board")
                self.board = TetrisBoard()
                self.board.spawn_piece()
        
        self.notify_observers()
        print("Tetris started")

    def pause(self):
        if self._running:
            self._running = False
            self.timer.stop()
            print("Tetris paused")

    def stop(self):
        self._running = False
        self.timer.stop()
        print("Tetris stopped")
    
    def switch_player(self):
        if len(self.players) > 1:
            self.active_player_index = (self.active_player_index + 1) % len(self.players)
            return True
        return False
    
    def get_active_player(self):
        if self.players and self.active_player_index < len(self.players):
            return self.players[self.active_player_index]
        return None
    
    # Processes input and updates game state
    def handle_input(self, key):
        if not self._running:
            return
            
        if key == 'LEFT':
            self.board.move_piece(0, -1)
        elif key == 'RIGHT':
            self.board.move_piece(0, 1)
        elif key == 'DOWN':
            if self.board.move_piece(1, 0):
                self.score += 1
        elif key == 'UP':
            self.board.rotate_piece()
        elif key == 'SPACE':
            while self.board.move_piece(1, 0):
                self.score += 2
            
            self.process_piece_lock()
        elif key == 'TAB':
            if self.switch_player():
                active_player = self.get_active_player()
                if active_player:
                    print(f"Active player: {active_player.name}")

    # Updates piece position based on timer
    def process_piece_lock(self):
        lines = self.board.lock_piece()
        if lines > 0:
            line_scores = [100, 300, 500, 800]
            points = line_scores[min(lines, 4) - 1] * self.level
            self.score += points
            self.lines_cleared += lines
            
            active_player = self.get_active_player()
            if active_player:
                active_player.update_score(points)
            
            self.level = (self.lines_cleared // 10) + 1
            
            self.move_delay = max(0.1, 1.0 - (self.level - 1) * 0.05)
        
        if not self.board.spawn_piece():
            self.game_over = True
            self.stop()
            
            active_player = self.get_active_player()
            if active_player:
                print(f"Game Over! Player {active_player.name}'s Final Score: {active_player.score}")
            else:
                print(f"Game Over! Final Score: {self.score}")

    def update(self):
        if not self._running or self.game_over:
            return
        
        if not self.board.current_piece and not self.game_over:
            if not self.board.spawn_piece():
                self.game_over = True
                self.stop()
                return
            
        elapsed = self.timer.get_time() - self.move_timer
        
        if elapsed >= self.move_delay:
            print(f"Moving piece down after {elapsed} seconds")
            if not self.board.move_piece(1, 0):
                self.process_piece_lock()
            
            self.move_timer = self.timer.get_time()
        
        self.notify_observers()
        
    def get_display_data(self):
        player_data = []
        for idx, player in enumerate(self.players):
            player_data.append({
                'name': player.name,
                'score': player.score,
                'is_active': idx == self.active_player_index
            })
            
        return {
            'board': self.board,
            'score': self.score,
            'level': self.level,
            'lines': self.lines_cleared,
            'next_piece': self.board.next_piece,
            'players': player_data
        }
