import streamlit as st
from streamlit_javascript import st_javascript
import json

def ok_click(scores, game_section, game_result_list):
    # Check for missing scores
    for idx, s in enumerate(scores):
        if s is None:
            st_javascript(f"alert('what is the score?'); document.getElementById('score_input_{idx}').focus();", key=f"alert_missing_score_{idx}")
            return
    # Check total score == 0
    if sum(scores) != 0:
        st_javascript("alert('wrong scoring');")
        return
    # Edit to game_result_list
    i = 0
    for s in scores:
        game_result_list[st.session_state["mp_selected_id"]][i] = int(s)
        i += 1

    js_update_results = f"window.localStorage.setItem('game_result_list', '{json.dumps(game_result_list)}');"
    st_javascript(js_update_results, key="edit_game_result_game_result_list_update")

    # Calculate total scores
    total_scores = [0, 0, 0, 0]
    for round_scores in game_result_list:
        for i in range(4):
            total_scores[i] += int(round_scores[i])

    # Update scores in game_section
    for i in range(4):
        game_section[i]['score'] = total_scores[i]

    # Save updated scores to window.localStorage
    js_update_section = f"window.localStorage.setItem('game_section', '{json.dumps(game_section)}');"
    st_javascript(js_update_section, key="edit_game_result_game_section_update")

    st.session_state.screen = "game"
    # st.rerun()

def edit_game_result_screen():
    st.title("Sửa điểm")
    # Load game_section from window.localStorage
    js_code = "window.localStorage.getItem('game_section')"
    game_section_json = st_javascript(js_code, key="edit_game_result_game_section")
    if not game_section_json:
        st.title("No game in progress.")
        return
    js_code_results = "window.localStorage.getItem('game_result_list')"
    game_result_list_json = st_javascript(js_code_results, key="edit_game_result_game_result_list")
    game_result_list = []
    if game_result_list_json:
        try:
            game_result_list = json.loads(game_result_list_json)
        except Exception:
            game_result_list = []
    
    selected_row = game_result_list[st.session_state["mp_selected_id"]] if st.session_state["mp_selected_id"] < len(game_result_list) else None
    if selected_row is None:
        st.error("No result selected.")
        return

    game_section = json.loads(game_section_json)
    scores = []
    cols = st.columns(4)
    for i, player in enumerate(game_section):
        score = cols[i].number_input(f"{player['name']}", key=f"score_input_{i}", value=selected_row[i], step=1, format="%d")
        scores.append(score)

    col_ok, col_cancel = st.columns([1,1])
    col_ok.button("OK", on_click=ok_click, args=[scores, game_section, game_result_list])
    cancel_clicked = col_cancel.button("Cancel")
    
    css = r'''
            <style>
                .stMainBlockContainer { padding: 2rem 1rem 2rem; }
                .stHorizontalBlock:first-of-type { padding-top: 20px;}
                div[class^='st-key-edit_game_result'], div[class*='st-key-edit_game_result']{height:0px;}
                div[class^='st-key-edit_game_result'] div, div[class*='st-key-edit_game_result'] div{height:0px;}
            </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    if cancel_clicked:
        st.session_state.screen = "game"
        st.rerun()
