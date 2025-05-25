import streamlit as st
from main_screen import main_screen
from new_game_screen import new_game_screen
from game_screen import game_screen
from game_result_screen import game_result_screen
from edit_game_result_screen import edit_game_result_screen

# Set page config
st.set_page_config(page_title="Game Score App", layout="wide")

# Initialize session state
if "screen" not in st.session_state:
    st.session_state.screen = "main"

# Screen router
def router():
    if st.session_state.screen == "main":
        main_screen()
    elif st.session_state.screen == "new_game":
        new_game_screen()
    elif st.session_state.screen == "game":
        game_screen()
    elif st.session_state.screen == "game_result":
        game_result_screen()
    elif st.session_state.screen == "edit_game_result":
        edit_game_result_screen()

router()