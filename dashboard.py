import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("⚽ Football Analytics Dashboard")

# load data
passes = pd.read_csv("data/passes.csv")
positions = pd.read_csv("data/player_positions.csv")

# show raw data
st.subheader("Pass Data")
st.write(passes.head())

# chemistry
st.subheader("Player Chemistry")

pair_counts = passes.groupby(["passer","receiver"]).size().reset_index(name="passes")

st.write(pair_counts)

# heatmap
st.subheader("Player Heatmap")

player_id = positions["player_id"].unique()[0]
player_data = positions[positions["player_id"] == player_id]

fig, ax = plt.subplots()

ax.hist2d(player_data["x"], player_data["y"], bins=50)

st.pyplot(fig)