import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Baseball Tracker Pro", layout="wide")

# App Title and Description
st.title("⚾ Baseball Tracker Pro")
st.markdown("Professional-grade statistics and game visualization.")

# Initialize session state
if 'game_data' not in st.session_state:
    st.session_state.game_data = []

# --- Input Section ---
with st.sidebar:
    st.header("Input Data")
    pitcher = st.text_input("Pitcher Name")
    batter = st.text_input("Batter Name")
    pitch_type = st.selectbox("Pitch Type", ["Fastball", "Curveball", "Slider", "Changeup", "Sinker"])
    result = st.selectbox("Result", ["Strike", "Ball", "Hit", "Out", "Walk", "HBP"])
    
    if st.button("Log Pitch"):
        new_entry = {"Pitcher": pitcher, "Batter": batter, "Type": pitch_type, "Result": result}
        st.session_state.game_data.append(new_entry)
        st.success("Pitch added!")

# --- Dashboard Section ---
if st.session_state.game_data:
    df = pd.DataFrame(st.session_state.game_data)
    
    # Stats Calculation
    total_pitches = len(df)
    strikes = len(df[df['Result'] == 'Strike'])
    balls = len(df[df['Result'] == 'Ball'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pitches", total_pitches)
    col2.metric("Strike %", f"{(strikes/total_pitches)*100:.1f}%" if total_pitches > 0 else "0%")
    col3.metric("Strike/Ball Ratio", f"{strikes/balls:.2f}" if balls > 0 else "N/A")

    # Data Display
    st.subheader("Game Log")
    st.dataframe(df, use_container_width=True)

    # Visualizations
    st.subheader("Visualizations")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Pitch Distribution")
        fig1, ax1 = plt.subplots()
        df['Type'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax1)
        st.pyplot(fig1)
        
    with c2:
        st.write("### Result Breakdown")
        fig2, ax2 = plt.subplots()
        df['Result'].value_counts().plot(kind='bar', ax=ax2, color='orange')
        st.pyplot(fig2)

    # Export CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Game Data (CSV)", csv, "game_data.csv", "text/csv")

else:
    st.info("Waiting for data... Enter your first pitch in the sidebar.")
