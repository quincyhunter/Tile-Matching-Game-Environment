# candycrush.py

from tmge import Game, GameBoard, Tile, Location
from observer import Subject
import random

# Available colors for game pieces
CANDY_TYPES = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"]

class CandyTile(Tile):
    # Represents a single candy piece with a color type
    def __init__(self, location=None, candy_type=None):
        super().__init__(location, 10)
        self.candy_type = candy_type if candy_type else random.choice(CANDY_TYPES)
        
    def __str__(self):
        return self.candy_type[0]
        
class CandyCrushBoard(GameBoard):
    # Manages the game board state and match detection
    def __init__(self, rows: int = 9, cols: int = 9):
        super().__init__(rows, cols)
        self.selected_tile = None
        self.matches = []
        self.populate_board()
        
    def populate_board(self):
        for i in range(self.plane.i_length):
            for j in range(self.plane.j_length):
                location = Location(i, j)
                tile = CandyTile(location)
                self.plane.set_tile(i, j, tile)
        
        self.resolve_initial_matches()
                
    def resolve_initial_matches(self):
        matches_found = True
        while matches_found:
            self.find_matches()
            if not self.matches:
                matches_found = False
            else:
                for i, j in self.matches:
                    current_tile = self.plane.get_tile(i, j)
                    available_types = list(CANDY_TYPES)
                    
                    if i > 1 and self.plane.get_tile(i-1, j) and self.plane.get_tile(i-2, j):
                        if (self.plane.get_tile(i-1, j).candy_type == 
                            self.plane.get_tile(i-2, j).candy_type and 
                            self.plane.get_tile(i-1, j).candy_type in available_types):
                            available_types.remove(self.plane.get_tile(i-1, j).candy_type)
                            
                    if j > 1 and self.plane.get_tile(i, j-1) and self.plane.get_tile(i, j-2):
                        if (self.plane.get_tile(i, j-1).candy_type == 
                            self.plane.get_tile(i, j-2).candy_type and 
                            self.plane.get_tile(i, j-1).candy_type in available_types):
                            available_types.remove(self.plane.get_tile(i, j-1).candy_type)
                    
                    if available_types:
                        current_tile.candy_type = random.choice(available_types)
                    else:
                        current_tile.candy_type = random.choice(CANDY_TYPES)
                
                self.matches = []

    def select_tile(self, i, j):
        if (0 <= i < self.plane.i_length and 
            0 <= j < self.plane.j_length):
            
            tile = self.plane.get_tile(i, j)
            if tile:
                if self.selected_tile:
                    selected_location = self.selected_tile.getLocation()
                    selected_i = selected_location.getI_Location()
                    selected_j = selected_location.getJ_Location()
                    
                    if ((abs(selected_i - i) == 1 and selected_j == j) or
                        (abs(selected_j - j) == 1 and selected_i == i)):
                        return self.swap_tiles(selected_i, selected_j, i, j)
                    else:
                        self.selected_tile = tile
                else:
                    self.selected_tile = tile
                return True
        return False
                
    def swap_tiles(self, i1, j1, i2, j2):
        tile1 = self.plane.get_tile(i1, j1)
        tile2 = self.plane.get_tile(i2, j2)
        
        if not tile1 or not tile2:
            return False
            
        tile1.candy_type, tile2.candy_type = tile2.candy_type, tile1.candy_type
        
        self.find_matches()
        
        if not self.matches:
            tile1.candy_type, tile2.candy_type = tile2.candy_type, tile1.candy_type
            self.selected_tile = None
            return False
            
        self.selected_tile = None
        return True
            
    def find_matches(self):
        self.matches = []
        
        for i in range(self.plane.i_length):
            j = 0
            while j < self.plane.j_length - 2:
                tile1 = self.plane.get_tile(i, j)
                if tile1:
                    match_length = 1
                    for k in range(j + 1, self.plane.j_length):
                        tile2 = self.plane.get_tile(i, k)
                        if tile2 and tile1.candy_type == tile2.candy_type:
                            match_length += 1
                        else:
                            break
                    
                    if match_length >= 3:
                        for k in range(j, j + match_length):
                            self.matches.append((i, k))
                        j += match_length
                    else:
                        j += 1
                else:
                    j += 1
        
        for j in range(self.plane.j_length):
            i = 0
            while i < self.plane.i_length - 2:
                tile1 = self.plane.get_tile(i, j)
                if tile1:
                    match_length = 1
                    for k in range(i + 1, self.plane.i_length):
                        tile2 = self.plane.get_tile(k, j)
                        if tile2 and tile1.candy_type == tile2.candy_type:
                            match_length += 1
                        else:
                            break
                    
                    if match_length >= 3:
                        for k in range(i, i + match_length):
                            self.matches.append((k, j))
                        i += match_length
                    else:
                        i += 1
                else:
                    i += 1
        
        self.matches = list(set(self.matches))
        return len(self.matches) > 0

    def remove_matches(self):
        if not self.matches:
            return 0
            
        match_count = len(self.matches)
        
        for i, j in self.matches:
            self.plane.clear_tile(i, j)
        
        self.apply_gravity()
        self.fill_empty_spaces()
        self.matches = []
        
        self.find_matches()
        
        return match_count
    
    def apply_gravity(self):
        for j in range(self.plane.j_length):
            for i in range(self.plane.i_length - 1, -1, -1):
                if not self.plane.get_tile(i, j):
                    for k in range(i - 1, -1, -1):
                        above_tile = self.plane.get_tile(k, j)
                        if above_tile:
                            self.plane.set_tile(i, j, above_tile)
                            location = above_tile.getLocation()
                            location.setI_Location(i)
                            self.plane.clear_tile(k, j)
                            i -= 1
    
    def fill_empty_spaces(self):
        for j in range(self.plane.j_length):
            for i in range(self.plane.i_length):
                if not self.plane.get_tile(i, j):
                    location = Location(i, j)
                    tile = CandyTile(location)
                    self.plane.set_tile(i, j, tile)

class CandyCrush(Game):
    # Main game controller handling scoring timers and multiplayer
    def __init__(self):
        super().__init__()
        self.board = CandyCrushBoard()
        self._running = False
        self.score = 0
        self.level = 1
        self.player_timers = {}
        self.default_time = 60  
        self.players = []
        self.game_over = False
        self.active_player_index = 0
        self.last_update_time = 0
        
    def add_player(self, player):
        self.players.append(player)
        self.player_timers[player] = self.default_time
        
    def switch_player(self):
        if len(self.players) > 1:
            previous_index = self.active_player_index
            self.active_player_index = (self.active_player_index + 1) % len(self.players)
            print(f"Switched from player {previous_index+1} to player {self.active_player_index+1}")
            print(f"Active player is now {self.players[self.active_player_index].name}")
            return True
        return False
    
    def get_active_player(self):
        if not self.players:
            return None
        return self.players[self.active_player_index]
        
    def get_opponent_player(self):
        if len(self.players) < 2:
            return None
        
        opponent_index = 1 - self.active_player_index  
        return self.players[opponent_index]
        
    def start(self):
        self._running = True
        self.timer.start()
        self.last_update_time = self.timer.get_time()
        
        for player in self.players:
            self.player_timers[player] = self.default_time
        
        if not self.board.plane.get_tile(0, 0):
            print("Initializing game board")
            self.board = CandyCrushBoard()
        else:
            # Check for empty cells
            empty_cells = 0
            for i in range(self.board.plane.i_length):
                for j in range(self.board.plane.j_length):
                    if not self.board.plane.get_tile(i, j):
                        empty_cells += 1
            
            if empty_cells > 0:
                print(f"Fixing board - found {empty_cells} empty cells")
                self.board = CandyCrushBoard()
        
        # One final check
        if not self.board.plane.get_tile(0, 0):
            print("Emergency board initialization")
            self.board = CandyCrushBoard()
            self.board.populate_board()
        
        self.notify_observers()
        print("Candy Crush started with timer system")

    def pause(self):
        if self._running:
            self._running = False
            self.timer.stop()
            print("Candy Crush paused")

    def stop(self):
        self._running = False
        self.timer.stop()
        print("Candy Crush stopped")

    def handle_input(self, i, j):
        if not self._running or self.game_over:
            return False
            
        print(f"Selected position ({i}, {j})")
        
        # Special case for testing
        if i == 99 and j == 99:
            if self.switch_player():
                active_player = self.get_active_player()
                if active_player:
                    print(f"Active player: {active_player.name}")
            return True
            
        if self.board.select_tile(i, j):
            print(f"Selected candy at ({i}, {j})")
            
            if self.board.matches:
                print(f"Found matches!")
                match_count, points = self.process_matches()
                
                active_player = self.get_active_player()
                if active_player:
                    active_player.update_score(points)
                    print(f"Updated {active_player.name}'s score to {active_player.score}")
                
                if len(self.players) > 1:
                    print(f"Switching players after move")
                    self.switch_player()
                    
                return True
        return False
    
    def process_matches(self):
        matches = self.board.remove_matches()
        points = matches * 10 
        total_match_count = matches
        
        cascade_multiplier = 1
        while self.board.matches:
            cascade_multiplier += 1
            additional_matches = self.board.remove_matches()
            total_match_count += additional_matches
            points += additional_matches * 10 * cascade_multiplier
        
        print(f"Found {total_match_count} matches total")
        
        self.score += points
        
        self.level = 1 + (self.score // 1000)
        
        if total_match_count > 0 and len(self.players) > 0:
            print(f"Adjusting timers for {len(self.players)} players")
            
            time_adjustment = 1
            
            active_player = self.get_active_player()
            if active_player:
                self.player_timers[active_player] += time_adjustment
                print(f"Added {time_adjustment} second to {active_player.name}'s timer")
                
            if len(self.players) > 1:
                opponent = self.get_opponent_player()
                if opponent:
                    self.player_timers[opponent] = max(1, self.player_timers[opponent] - time_adjustment)
                    print(f"Reduced {opponent.name}'s timer by {time_adjustment} second")
        
        return total_match_count, points
    
    def end_game(self):
        self.game_over = True
        self.stop()
        
        print(f"Game Over!")
        
        for player in self.players:
            print(f"Player {player.name}: {player.score}")
    
    def update(self):
        if not self._running:
            return
            
        current_time = self.timer.get_time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        active_player = self.get_active_player()
        if active_player:
            self.player_timers[active_player] -= elapsed
            
            if self.player_timers[active_player] <= 0:
                self.player_timers[active_player] = 0
                
                if len(self.players) > 1:
                    opponent = self.get_opponent_player()
                    if opponent:
                        opponent.update_score(500)
                        print(f"Time's up! {opponent.name} wins!")
                else:
                    print(f"Time's up! Game over for {active_player.name}")
                
                self.end_game()
        
        self.notify_observers()
        
    def get_display_data(self):
        player_data = []
        for idx, player in enumerate(self.players):
            time_left = int(self.player_timers.get(player, self.default_time))
            player_data.append({
                'name': player.name,
                'score': player.score,
                'is_active': idx == self.active_player_index,
                'time_left': time_left
            })
            
        active_player = self.get_active_player()
        time_left = int(self.player_timers.get(active_player, self.default_time)) if active_player else self.default_time
            
        return {
            'board': self.board,
            'score': self.score,
            'level': self.level,
            'time_left': time_left,
            'players': player_data
        }
