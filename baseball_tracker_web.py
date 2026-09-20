import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto-Scout Scorebook", layout="wide")

# --- Initialize Game State ---
defaults = {
    'score_home': 0, 'score_away': 0, 'hits': 0, 'errors': 0, 'inning': "1 Top"
}
for key, val in defaults.items():
    if key not in st.session_state: st.session_state[key] = val

if 'log' not in st.session_state:
    st.session_state.log = pd.DataFrame(columns=['Event', 'Inning', 'Score', 'Result'])

st.title("⚾ Auto-Scout Scorebook")

# --- Sidebar: Action Center ---
with st.sidebar:
    st.header("Game Actions")
    inning_select = st.selectbox("Current Inning", ["1 Top", "1 Bot", "2 Top", "2 Bot", "3 Top", "3 Bot", "4 Top", "4 Bot", "5 Top", "5 Bot", "6 Top", "6 Bot", "7 Top", "7 Bot", "8 Top", "8 Bot", "9 Top", "9 Bot"])
    
    st.divider()
    action = st.radio("What happened?", ["Pitch (Ball/Strike)", "Hit", "Run Scored", "Error", "Out"])
    
    if st.button("Log Event"):
        st.session_state.inning = inning_select
        
        # Logic to update scoreboard automatically
        if action == "Hit": st.session_state.hits += 1
        elif action == "Run Scored": st.session_state.score_home += 1
        elif action == "Error": st.session_state.errors += 1
        
        # Add to historical log
        new_entry = pd.DataFrame({
            'Event': [action], 
            'Inning': [st.session_state.inning], 
            'Score': [f"{st.session_state.score_away}-{st.session_state.score_home}"],
            'Result': [action]
        })
        st.session_state.log = pd.concat([st.session_state.log, new_entry], ignore_index=True)
        st.rerun()

    st.divider()
    if st.button("Reset Game"):
        for key in defaults: st.session_state[key] = defaults[key]
        st.session_state.log = pd.DataFrame(columns=['Event', 'Inning', 'Score', 'Result'])
        st.rerun()

# --- Main Dashboard ---
# Scoreboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Score", f"{st.session_state.score_away}-{st.session_state.score_home}")
col2.metric("Hits", st.session_state.hits)
col3.metric("Errors", st.session_state.errors)
col4.metric("Inning", st.session_state.inning)

st.write("---")

# The "Game Text" (Play-by-Play)
st.subheader("Play-by-Play Record")
st.dataframe(st.session_state.log.sort_index(ascending=False), use_container_width=True)

# Export
csv = st.session_state.log.to_csv(index=False).encode('utf-8')
st.download_button("Export Official Scorebook (CSV)", csv, "scorebook.csv", "text/csv")
