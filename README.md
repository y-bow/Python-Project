# Chess Pro - Python Chess Game

A modern, high-performance Chess application built with Python, Pygame, and the `python-chess` library. This project features a sleek, fullscreen user interface with dynamic scaling and integrated game timers.

![Chess Pro Preview](https://via.placeholder.com/800x450?text=Chess+Pro+Gameplay+Preview)

## 🌟 Features

- **Premium UI**: Designed with a deep, modern color palette and smooth visual feedback.
- **Dynamic Scaling**: Automatically adjusts to your screen resolution for a perfect fit in fullscreen mode.
- **Integrated Timers**: Competitive 10-minute countdown timers for both players.
- **Legal Move Highlighting**: Visual indicators for all possible moves when a piece is selected.
- **Comprehensive Rules**: Supports checkmate, stalemate, and automatic pawn promotion (to Queen).
- **Smooth Gameplay**: Optimized 60 FPS rendering for a fluid experience.
- **Global Controls**: Easy reset and exit functionality.

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/y-bow/Python-Project.git
   cd Python-Project
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame python-chess
   ```
   *(Alternatively, if `requirements.txt` is provided, use: `pip install -r requirements.txt`)*

## 🚀 How to Run

Launch the game by running the main script:

```bash
python pygame_chess.py
```

## 🎮 Controls

| Action | Control |
| :--- | :--- |
| **Select Piece** | Left Mouse Click |
| **Move Piece** | Left Mouse Click on Target Square |
| **Reset Game** | Press `R` Key |
| **Exit Game** | Press `ESC` Key or Close Window |

## 📁 Project Structure

```
Python Project/
├── pygame_chess.py      # Main game logic and UI
├── requirements.txt     # Project dependencies
├── static/
│   └── images/
│       └── pieces/      # High-quality chess piece assets
└── README.md            # You are here!
```

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
