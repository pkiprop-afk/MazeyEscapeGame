# MazeyEscapeGame
Mazey- The Maze Escape is a maze game built in Python using the Pygame Library. 
The core idea of the game is trying to escape the maze before time runs out while enemies are chasing you.
You must navigate the maze armed only with a draining flashlight, navigating corridors, avoiding patrol enemies, collecting powerups and reaching the exit before time runs out.

# Game Features
The player character has a flashlight
There are three difficulty levels to choose from: Easy, Hard and Veteran each with different features fitting the level of players
There are two enemy types: Patrol Enemies and Guard Enemies each with different functions
There are six unique power ups:
    Slow Time - slows all enemies for 8 seconds
    Speed Boost - increases player movement speed for 6 seconds
    Weapons - Player acquires a random weapon with limited ammo
    Teleport - Instantly swaps  your position with a random Patrol Enemy
    Freeze Gun - Freezes all enemies for 5 seconds
    Auto Win - Instantly teleports the player to the exit for an automatic victory

# Controls
W / UP Arrow - Move Up
A / DOWN Arrow - Move Down
S / LEFT Arrow - Move Left
D / RIGHT Arrow - Move Right
Shoot Weapon - SPACE(Only works when you have a weapon)
Select/ Confirm - ENTER

# FILE STRUCTURE
## Mazey_main.py
Contains the files to start the game
We imported the Game class, defined a function <main()>, made an instance of the class Game and ran the game.

## Mazey_constants.py
This file contains all the constants that are used in the game.

## Mazey_builder.py
Build the game map, entities, and powerups for a given difficulty level.

    This function translates the tile-based map data into sprite groups, a player
    instance, and supporting structures used to run a game session.

    Args:
        difficulty_key: The key used to select difficulty settings from DIFFICULTY.

    Returns:
        A tuple containing:
        - walls: Sprite group of wall tiles.
        - goals: Sprite group of goal/exit tiles.
        - all_enemies: Sprite group containing all enemy instances.
        - patrol_list: List of patrol enemy instances.
        - guard_list: List of guard enemy instances.
        - powerups: Sprite group of powerup instances.
        - player: The player instance positioned on the map.
        - floor_rects: List of floor rectangles used for drawing and placement.
