# Game Score App

A modular Streamlit application for tracking scores of a 4-player game, with persistent storage using browser localStorage.

## Features

- Modular screens: Main, New Game, Game, Add Game Result
- Persistent storage via browser localStorage (using `streamlit_javascript`)
- Input validation and alerts
- Score history and total calculation

## Requirements

- Python 3.8+
- [streamlit](https://streamlit.io/)
- [streamlit_javascript](https://github.com/blackary/streamlit-javascript)

## Installation

```bash
pip install streamlit streamlit_javascript
```

## Running the App

```bash
streamlit run app.py
```

## File Structure

- `app.py` — Main controller and router
- `main_screen.py` — Main screen
- `new_game_screen.py` — New game setup
- `game_screen.py` — Game play and score table
- `game_result_screen.py` — Add round result
- `README.md` — This file

## Notes

- All data is stored in your browser's localStorage.
- To reset, use the "New Game" button or clear your browser storage.