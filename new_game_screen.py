import streamlit as st
from streamlit_javascript import st_javascript
import json

def ok_click(player_names):
    for idx, name in enumerate(player_names):
        if not name.strip():
            st_javascript(f"alert('What is player name?'); document.getElementById('player_name_{idx}').focus();", key=f"alert_missing_name_{idx}")
            return
    # All names provided, initialize game_section and game_result_list
    game_section = [{"name": n.strip(), "score": 0} for n in player_names]
    value = json.dumps(game_section, ensure_ascii=False)
    js_set_section = f"window.localStorage.setItem('game_section', '{value}');"
    js_clear_results = "window.localStorage.setItem('game_result_list', '[]');"
    st_javascript(js_set_section, key="new_game_game_section")
    st_javascript(js_clear_results, key="new_game_game_result_list")
    st.session_state.screen = "game"
    st.rerun()

def new_game_screen():
    st.title("New Game")
    # Load game_section from window.localStorage
    js_code = "window.localStorage.getItem('game_section')"
    game_section_json = st_javascript(js_code, key="main_game_section")
    game_section = None
    if game_section_json:
        try:
            game_section = json.loads(game_section_json)
        except Exception:
            game_section = None
    player_names = []
    for item in game_section:
        if item and 'name' in item:
            player_names.append(item['name'])

    focus_idx = None

    # Four text inputs for player names
    cols = st.columns(4)
    for i in range(4):
        name = cols[i].text_input(f"Player {i+1}", key=f"player_name_{i}", value=player_names[i] if i < len(player_names) else "", max_chars=20)
        player_names.append(name)

    col_ok, col_cancel = st.columns([1,1])
    col_ok.button("OK", on_click=ok_click, args=[player_names])
    cancel_clicked = col_cancel.button("Cancel")
    
    css = r'''
            <style>
                .stMainBlockContainer { padding: 2rem 1rem 2rem; }
                div[class^='st-key-new_game'], div[class*='st-key-new_game']{height:0px;}
            </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    if cancel_clicked:
        st.session_state.screen = "main"
        st.rerun()