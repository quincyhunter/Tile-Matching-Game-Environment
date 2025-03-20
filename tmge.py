from abc import ABC, abstractmethod
import time
from observer import Subject


class Player:
    """
    Represents a player profile in the TMGE
    """
    def __init__(self, name: str = "Unknown"):
        self._name = name
        self._score = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def score(self) -> int:
        return self._score

    def update_score(self, value: int) -> None:
        self._score += value

class Location:
    """
    Represents a location on the grid
    """
    def __init__(self, i_coordinate: int = 0, j_coordinate: int = 0):
        self._i_coordinate = i_coordinate
        self._j_coordinate = j_coordinate

    def getI_Location(self) -> int:
        return self._i_coordinate

    def setI_Location(self, i: int) -> None:
        self._i_coordinate = i

    def getJ_Location(self) -> int:
        return self._j_coordinate

    def setJ_Location(self, j: int) -> None:
        self._j_coordinate = j

class Tile:
    """
    Represents an individual tile on the game board
    """
    def __init__(self, location = None, points: int = 0):
        self._location = location if location else Location()
        self._points = points

    def getLocation(self) -> Location:
        return self._location

    def setLocation(self, loc: Location) -> None:
        self._location = loc

    @property
    def points(self) -> int:
        return self._points

    @points.setter
    def points(self, val: int) -> None:
        self._points = val

class Grid:
    """
    Represents the grid which has tiles
    """
    def __init__(self, i_length: int, j_length: int):
        self.i_length = i_length
        self.j_length = j_length
        # 2D list to store Tile objects or None
        self.matrix = [
            [None for _ in range(j_length)] for _ in range(i_length)
        ]

    def get_tile(self, i: int, j: int):
        if 0 <= i < self.i_length and 0 <= j < self.j_length:
            return self.matrix[i][j]
        return None

    def set_tile(self, i: int, j: int, tile: Tile) -> None:
        if 0 <= i < self.i_length and 0 <= j < self.j_length:
            self.matrix[i][j] = tile

    def clear_tile(self, i: int, j: int) -> None:
        if 0 <= i < self.i_length and 0 <= j < self.j_length:
            self.matrix[i][j] = None

class GameBoard:
    """
    Represents the game board
    """
    def __init__(self, rows: int, cols: int):
        self.plane = Grid(rows, cols)

    def get_grid(self) -> Grid:
        return self.plane


class Timer:
    def __init__(self):
        self._start_time = None
        self._elapsed = 0

    def start(self):
        if self._start_time is None:
            self._start_time = time.time()

    def stop(self):
        if self._start_time is not None:
            self._elapsed += time.time() - self._start_time
            self._start_time = None

    def reset(self):
        self._start_time = None
        self._elapsed = 0

    def get_time(self) -> float:
        total = self._elapsed
        if self._start_time is not None:
            total += (time.time() - self._start_time)
        return total


class Menu:
    """
    Represents a menu system which can create or load games
    """
    def __init__(self):
        self.available_games = []

    def register_game(self, game_class):
        self.available_games.append(game_class)

    def new_game(self, game_class):
        return game_class()

    def load_game(self, game_class):
        return game_class()


class Game(Subject, ABC):
    """
    Base Game class
    """
    def __init__(self):
        super().__init__()  
        self.timer = Timer()
        self._running = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def update(self):
        pass
