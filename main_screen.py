import streamlit as st
from streamlit_javascript import st_javascript
import json
import pandas as pd

def main_screen():
    st.title("Game Score")
    # Load game_section from window.localStorage
    js_code = "window.localStorage.getItem('game_section')"
    game_section_json = st_javascript(js_code, key="main_game_section")
    game_section = None
    if game_section_json:
        try:
            game_section = json.loads(game_section_json)
        except Exception:
            game_section = None

    if game_section:
        st.subheader("Current Game")
        # Convert to a single dictionary inside a list
        converted = [{item["name"]: item["score"] for item in game_section}]

        # Load into DataFrame
        df = pd.DataFrame(converted)

        st.table(df)
        css = r'''
            <style>
                .stMainBlockContainer { padding: 2rem 1rem 2rem; }
                table th {width: 20% !important;}
                table td {text-align: center !important;}
                div[class^='st-key'], div[class*='st-key']{height:0px;}
            </style>
        '''
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.title("No current game. Start a new game!")

    col_new, col_open = st.columns([1,1])
    new_clicked = col_new.button("New Game")
    open_clicked = col_open.button("Open Game")

    if new_clicked:
        st.session_state.screen = "new_game"
        st.rerun()
    if open_clicked:
        st.session_state.screen = "game"
        st.rerun()