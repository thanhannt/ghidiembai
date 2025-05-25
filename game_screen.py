import streamlit as st
from streamlit_javascript import st_javascript
import json
import pandas as pd

def single_row_selection_callback():
    st.session_state["mp_single_row_selection_callback"] = True


def game_screen():
    st.title("Đang chơi")
    # Load game_section and game_result_list from window.localStorage
    js_code_section = "window.localStorage.getItem('game_section')"
    js_code_results = "window.localStorage.getItem('game_result_list')"
    game_section_json = st_javascript(js_code_section, key="game_game_section")
    game_result_list_json = st_javascript(js_code_results, key="game_game_result_list")

    if not game_section_json:
        st.warning("No game in progress.")
        # st.session_state.screen = "main"
        # st.rerun()
        return

    game_section = json.loads(game_section_json)
    game_result_list = []
    if game_result_list_json:
        try:
            game_result_list = json.loads(game_result_list_json)
        except Exception:
            game_result_list = []

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
    st_javascript(js_update_section, key="game_game_section_update")

    # Table display
    st.markdown("#### Tổng điểm hiện tại:")
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
            div[class^='st-key'] div, div[class*='st-key'] div{height:0px;}
        </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    if game_result_list:
        st.markdown("##### Các lượt chơi:")
        df = pd.DataFrame(columns=df.columns)

        for idx, round_scores in enumerate(game_result_list):
            df.loc[len(df)] = [str(round_scores[i]) for i in range(4)]
        # st.table(df)
        event = st.dataframe(
            df,
            on_select=single_row_selection_callback,
            selection_mode="single-row",
        )

        modules = event.selection.rows
        
        if st.session_state.get("mp_single_row_selection_callback", False) is True:
            st.session_state["mp_single_row_selection_callback"] = False
            st.session_state["mp_selected_id"] = modules[0] if len(modules) > 0 else None
            if st.session_state["mp_selected_id"] is not None:
                st.cache_data.clear()
                st.session_state.screen = "edit_game_result"
                st.rerun()

    col_end, col_add = st.columns([1,1])
    if col_end.button("Kết thúc"):
        st.session_state.screen = "main"
        st.rerun()
    if col_add.button("Thêm điểm"):
        st.session_state.screen = "game_result"
        st.rerun()