# Icy Tower Remake

A Python remake of the classic Icy Tower platformer, built with Pygame. The player jumps between platforms, climbing as high as possible without falling.

---

## Demo

> *Add a GIF or screenshot here — e.g., a screen recording of the gameplay*

---

## Features

- Scrolling platformer physics (gravity, jump, collision)
- Main menu with navigation and a finger-selector cursor
- Instructions screen
- High score tracking (saved to `Notes/scores.json`)
- Custom fonts and background art
- Clean screen-based architecture (Menu → Game → back to Menu)

---

## Tech Stack

| | |
|---|---|
| Language | Python 3.12 |
| Graphics & Input | Pygame 2.6 |
| Data | JSON (scores) |

---

## Project Structure

```
icytower_remake/
├── Program.py            # Entry point — runs the full game
├── main.py               # Standalone physics prototype
├── Screens/
│   ├── Menu.py           # Main menu screen
│   ├── Game.py           # Core game loop and logic
│   └── Instructions.py   # How-to-play screen
├── DataModels/
│   ├── Player.py         # Player state and physics
│   ├── Platforms.py      # Platform logic
│   └── GameObject.py     # Base game object
├── settings/
│   └── Config.py         # Global constants (screen size, colors, fonts)
├── Game_images/          # Background and game-over assets
├── Menu_images/          # Menu backgrounds and UI elements
├── Instructions_images/  # Keyboard diagrams
├── Fonts/                # Custom TTF/OTF fonts
└── Notes/
    └── scores.json       # Persisted high scores
```

---

## Getting Started

**Requirements:** Python 3.10+

```bash
# Clone the repository
git clone https://github.com/yuyuber12/icytower_remake.git
cd icytower_remake

# Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate   # Windows
# or: source .venv/bin/activate  (macOS/Linux)

pip install pygame

# Run the game
python Program.py
```

---

## Controls

| Key | Action |
|---|---|
| ← → | Move left / right |
| Space | Jump |
| Esc | Back to menu |

---

## How It Works

The game runs a loop between three screens managed by `Program.py`:

1. **Menu** — navigate options with arrow keys and Space
2. **Game** — physics-based platformer with scrolling camera
3. **Instructions** — keyboard reference screen

Platform generation, player physics, and score saving are handled in the `Screens/Game.py` and `DataModels/` modules.

---

## What I Learned

- Implementing a 2D physics system (gravity, velocity, collision resolution) from scratch
- Designing a multi-screen game loop with state management
- Separating game logic into reusable data models
- Persisting and loading data with JSON
