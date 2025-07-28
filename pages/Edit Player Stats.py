import streamlit as st
import pandas as pd
import os

st.title("📝 Edit Player Stats")

# Load data
if os.path.exists("players.csv"):
    df = pd.read_csv("players.csv")
else:
    st.error("No players.csv file found. Please add players first.")
    st.stop()

if df.empty:
    st.warning("No players found in players.csv. Please add players first.")
    st.stop()

# Select player to edit
selected_player = st.selectbox("Select a player to edit:", df["name"].tolist())
player_data = df[df["name"] == selected_player].iloc[0]

# Show player name but disable editing it (optional)
st.text(f"Player Name: {selected_player}")

# Edit stats with sliders
updated_stats = {}
for stat in df.columns[1:]:
    updated_stats[stat] = st.slider(f"{stat.capitalize()}", 1, 5, int(player_data[stat]), key=stat)

# Save button
if st.button("💾 Save Changes"):
    # Update dataframe with new stats
    for stat, value in updated_stats.items():
        # Ensure the value matches the column's data type
        df.loc[df["name"] == selected_player, stat] = value
    df.to_csv("players.csv", index=False)
    st.success(f"✅ {selected_player}'s stats updated!")
    st.experimental_rerun()
