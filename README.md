# X in a Line Bot Challenge

Welcome to the X in a Line Bot Challenge, a project developed for the Computer Systems course at the University of Southern Denmark.

## Installation

Assuming you have the file the following steps needed to be done before you can start your project:

1. Install dependencies from `requirements.txt` using the command line interface and pip:
   ```bash
   pip install -r requirements.txt
   ```
   **OR, using Thonny:**

   Menu->Tools->Manage Packages...-> type *pygame* -> press *Search* -> select _pygame_ -> press *Install*

2. Run the game:
   ```bash
   python main.py
   ```

## Writing your bot

1. Before you do anything, make sure to run the `main.py` file at least once. You should see a `settings.json` file in the root directory afterward.

2. Find the `bots/team_your_name_bot.py` file. All of your code will be written here. Feel free to rename this file to reflect the name of your bot.

3. In this file, you will find a `TeamYourNameBot` class. This is the class you will modify. You can rename this class as well.

4. Customize the `__init__` method to personalize your bot. Set the `bot_name` and choose an RGB color for your bot.

5. The `init_board` method will run at the beginning of the game. By invoking the function, the game will "let the bot know" the board's dimensions, the obstacles' location and the time your bot gets for the whole game. You may want to store them; they will come in handy later.

6. The `notify_move` method is called when a move is made by any player. You can add additional code here if needed. It is probably a good idea to store those moves somewhere.

7. The core of your bot's logic lies in the `make_a_move` method. Implement your algorithm to decide the best move for your bot.

8. To be able to try your bot, you need to adjust some settings. First, in the `game/settings.py` file, you must modify the import to reflect the new names you set earlier. Change the name of the library and the name of the class.
   ```Python
   # Change this line:
   from bots.team_your_name_bot import TeamYourNameBot
   # To this for A team:
   from bots.team_a_bot import TeamABot
   ```
   You will not need to touch this file again if you don't change the file or the class name again.

9. Open the `settings.json` file. You will find many settings here; you can read about them in the **Settings** section. Find the entry called `BOTS`. Remove the old `TeamYourNameBot` entry and add your new bot. The name of the class must be written here as a string.

### Good to know
The indexing of the board starts at (0, 0) in the top left corner. The x coordinate represents the horizontal, and the y the vertical axis.

## Rules

### Objective
The game is played on a grid where players take turns to place their symbol in an empty cell. The goal is to achieve a line of consecutive symbols horizontally, vertically, or diagonally.

### Game Setup
The number of rows and columns can change from game to game, and the starting board might have some already occupied cells.

### Players
Any number of players can participate in the game. If a player is disqualified, the game continues without it. The order in which the players take turns will be determined at the start.

### Winning Conditions
The winner is the first player to achieve the required `WIN_LENGTH` (set in the `settings.json` file).

### Programming resources
You can only use the built-in Python libraries.

### Disqualification
Violating the following rules will result in disqualification for the offending bot:
   - The bots must make a move within the board.
   - The bots must place a symbol on an empty cell.
   - The bots must be able to calculate the move with the given limited resources.
   - Each bot gets a certain amount of time for the whole game. They must finish every calculations within this time limit. The `GAME_TIME` setting sets the limit.
   - Your code must not raise an exception.
   - The bots are not allowed to access the internet. Every computation must be done locally.

## Settings
Explore and customize the game settings in the `settings.json` file. If the file is missing, please run the game once, run the main.py.

### Graphics Settings
Adjust the visual aspects of the game.

- **CELL_SIZE:** The size of each cell in pixels.
- **LINE_WIDTH:** The width of the grid lines in pixels.

### Colors
Customize the color scheme of the game.

- **WHITE:** RGB values for the color white. 
- **BLACK:** RGB values for the color black.
- **FONT_COLOR:** RGB values for font color.
- **LINE_COLOR:** RGB values for grid line color.
- **BACKGROUND_COLOR:** RGB values for the background color.
- **WINNING_LINE_COLOR:** RGB values for the winning line color.

### Game Settings
Configure various gameplay options.

- **FAST_MODE:** By enabling it, the game will be played automatically until the end.
- **SHUFFLE_PLAYERS_ON_START:** Shuffle the order of players at the start of each game.
- **CHANCE_OF_BLOCKED_ON_START:** Probability of a cell being taken at the beginning.
- **RESTART_DELAY:** Press SPACE to restart the game. For RESTART_DELAY > 0, pressing SPACE pauses automatic restarting.
- **KEY_DELAY:** If you keep holding the _SPACE_ key at the end of the game, the game will wait before restarting. Because of the way Pygame works, it needs a bit of time to detect key presses. This entry sets this time. You don't need to modify it.
- **GAME_TIME:** The time a bot gets for calculations for the game. Represented in nanoseconds.

### Board Settings
Define the board dimensions.

- **BOARD_WIDTH:** Number of cells horizontally
- **BOARD_HEIGHT:** Number of cells vertically
- **WIN_LENGTH:** Number of consecutive cells needed to win.

### Winning Conditions
Choose the winning conditions.

- **WIN_HORIZONTAL**: Enable or disable horizontal wins.
- **WIN_VERTICAL**: Enable or disable vertical wins.
- **WIN_DIAG_POS**: Enable or disable positive diagonal wins.
- **WIN_DIAG_NEG**: Enable or disable negative diagonal wins.

### Player List
Specify the bots to be included in the game.
- **BOTS:** A list containing the names of the classes participating in the game. A bot can be part of a game any number of times.
Note: Every class on the `BOTS` list needs to be a subclass of `BaseBot`

## Reporting bugs
If you find a bug, please let us know. 

Best of luck with the X in a Line Bot Challenge!