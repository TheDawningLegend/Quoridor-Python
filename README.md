# Quoridor (Python)

A digital implementation of the board game **Quoridor**, built with Python and Pygame.

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/958ac9fb-fd02-4ac2-9fc0-cab98e885727" />

## 🎮 Gameplay Overview

Quoridor is a strategic board game where two players race to reach the opposite side of the board while placing walls to slow down their opponent.

Each player can:
- Move one square per turn (up, down, left, right)
- Place walls to block paths
- Jump over the opponent when adjacent

## 🧠 Rules

### Objective
Be the first player to reach the opposite side of the board:
- Blue player starts at the top and aims for the bottom
- Red player starts at the bottom and aims for the top

### Movement
On each turn, a player can:
- Move to an adjacent square (no diagonals)
- Jump over the opponent if directly adjacent (if not blocked)
- Move diagonally when a jump is blocked by a wall

Walls block movement between squares.

### Walls
- Each player starts with a limited number of walls
- Walls are placed between squares
- Walls cannot:
  - Overlap
  - Cross each other
  - Fully block a player’s path to the goal

## 🎮 Controls

- **Left Click** → Move / Place wall
- **R Key** → Restart game

## 🚀 How to Run

### Install dependencies
```bash
pip install pygame
