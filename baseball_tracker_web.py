import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Baseball Tracker Pro", layout="wide")

st.title("⚾ Baseball Tracker Pro")

# Initialize session state for game data
if 'game_data' not in st.session_state:
    st.session_state.game_data = []

# Sidebar for Input
with st.sidebar:
    st.header("Enter Pitch Data")
    pitcher = st.text_input("Pitcher Name")
    pitch_type = st.selectbox("Pitch Type", ["Fastball", "Curveball", "Slider", "Changeup", "Other"])
    result = st.selectbox("Result", ["Strike", "Ball", "Hit", "Out", "Walk"])
    
    if st.button("Add Pitch"):
        st.session_state.game_data.append({
            "Pitcher": pitcher, 
            "Type": pitch_type, 
            "Result": result
        })
        st.success("Pitch saved!")

# Main Dashboard
if st.session_state.game_data:
    df = pd.DataFrame(st.session_state.game_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Game Log")
        st.dataframe(df)
        
    with col2:
        st.subheader("Pitch Summary")
        pitch_counts = df['Type'].value_counts()
        fig, ax = plt.subplots()
        pitch_counts.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("Pitch Distribution")
        st.pyplot(fig)
else:
    st.info("Start adding pitches to see stats and charts!")
