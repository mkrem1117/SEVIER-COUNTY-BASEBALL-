import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Baseball Tracker Pro")

if 'game_data' not in st.session_state:
    st.session_state.game_data = []

pitcher = st.text_input("Pitcher Name")
pitch_type = st.selectbox("Pitch Type", ["Fastball", "Curveball", "Slider", "Changeup"])
result = st.selectbox("Result", ["Strike", "Ball", "Hit", "Out"])

if st.button("Add Pitch"):
    st.session_state.game_data.append({"Pitcher": pitcher, "Type": pitch_type, "Result": result})
    st.success("Pitch added!")

if st.session_state.game_data:
    df = pd.DataFrame(st.session_state.game_data)
    st.write("### Game Log", df)
