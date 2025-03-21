# Tile-Matching Game Environment (TMGE)

## Overview

The goal of this project is to create a game environment for developing simple tile-matching games similar to that of Tetris, Dr. Mario, and Candy Crush. This project is to designed and developed using the skills and design strategies learned in the course IN4MATX 122.

## Currently Supported Games

Currently, our environment includes only two fully implemented games:
1. **Tetris**
2. **Candy Crush**

But many more games can be created by using this environment to develop further.

## Instructions on How to Run

1. Make sure you have Python installed, you may need a newer version if having issues.
2. Open the ZIP file from the canvas submission with a IDE of your choosing.
3. Ensure you cd to the correct directory, this should be `Tile-Matching-Game-Environment` or similar.
4. You can now run the TMGE by running `python main.py`.
5. Select any game from the menu.
6. Select the number of players (1 or 2).
7. Enter each player name and select the `Start Game` button.

## User Controls

### Tetris

#### <u>Gameplay Notes</u>
- Clear lines by filling entire rows with blocks
- Score is increased based on number of lines cleared at once
- Level increases after clearing every 10 lines 
- Speed increases with each level
- Game ends when blocks reach the top of the screen

#### <u>Single Player</u>

- **←/→**: Move piece left/right
- **↓**: Move piece down faster
- **↑**: Rotate piece
- **Space**: Instant drop / placement

#### <u>Multiplayer</u>

Multiplayer mode enables a split screen view where players can compete against each other in real-time. Both players compete to achieve the highest score in a game and the winner is decided once a player fails or the time allotted runs out.

- `Player 1`uses WASD controls on the left side 

  **W** - Rotate piece

  **A / D** - Move piece left/right

  **S** - Move piece down faster 

  **Spacebar** - Instant drop / placement
  
- `Player 2` uses the default single player controls (arrows and spacebar)

### Candy Crush

#### <u>Gameplay Notes</u>
- Swap adjacent candies to create matches of 3 or more
- Matches clear candies and award points
- Creating matches adds time to your timer
- In multiplayer mode, matches reduce your opponent's time
- Game ends when time runs out


#### <u>Single Player</u>

- **←/→/↑/↓**: Move cursor 
- **Space**: Select/swap candy
- Match 3+ candies in a row or column to clear them
- Time-based gameplay: Make matches to add time

#### <u>Multiplayer</u>


#### Player 1 (Left Screen)
- **W/A/S/D**: Move cursor or piece
- **Space**: Select/drop

#### Player 2 (Right Screen)
- **Arrow Keys**: Move cursor or piece
- **Enter**: Select/drop


## TMGE Design

**Core Environment Components**:
  - **Game**: Abstract base class for all games
  - **GameBoard**: Manages the game playing field
  - **Grid**: Gives structure to GameBoard
  - **Tile**: Game piece on grid
  - **Location**: Position on the grid
  - **Player**: A named user with their respective stats (score)
  - **Timer**: Game clock
  - **Menu**: Game landing page

**GUI Components**:
  - **TkinterGUI**: Basic windowed interface for the environment
  - **TetrisGUI**: UI for Tetris game
  - **CandyCrushGUI**: UI for Candy Crush game
  - **SplitScreenMultiplayerGUI**: Split screen interface for multiple players

### Design Pattern Implemented

In our TMGE, we implemented a observer design pattern to ensure we are constantly updated other components of our game with what the current and most up-to-date game state is. 

<u>Observer Pattern</u>

**Subject** - Game

**Observer** - GameBoard, Grid, Tile, Location, Player, Timer, Menu

The Game component acts as the Subject that notify registered Observers of state changes
- For Example, UI components like TkinterGUI implement the Observer interface

### Libraries

Below are the list of libraries used which are self explanatory:
1. Tkinter
2. ABC (Abstract Base Class)
2. Time
3. OS
4. Sys
5. Subprocess
6. Random