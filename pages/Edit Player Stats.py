import streamlit as st
import pandas as pd
import os

st.title("📝 Edit or Add Player Stats")

# Load data
if os.path.exists("players.csv"):
    df = pd.read_csv("players.csv")
else:
    df = pd.DataFrame(columns=["name", "tech", "strength", "control", "finish", "stamina"])

# Tabs: Edit existing or Add new
tab1, tab2 = st.tabs(["✏️ Edit Player", "➕ Add New Player"])

with tab1:
    if df.empty:
        st.warning("No players found. Please add new players first.")
    else:
        selected_player = st.selectbox("Select a player to edit:", df["name"].tolist())
        player_data = df[df["name"] == selected_player].iloc[0]

        updated_stats = {}
        for col in df.columns[1:]:
            updated_stats[col] = st.slider(
                f"{col.capitalize()}",
                1, 5, int(player_data[col])
            )

        if st.button("💾 Save Changes"):
            for stat in updated_stats:
                df.loc[df["name"] == selected_player, stat] = updated_stats[stat]
            df.to_csv("players.csv", index=False)
            st.success(f"Stats for {selected_player} updated!")

with tab2:
    st.subheader("Add a new player")
    new_name = st.text_input("👤 Player Name")

    new_stats = {}
    for col in df.columns[1:]:
        new_stats[col] = st.slider(f"{col.capitalize()}", 1, 5, 3)

    if st.button("➕ Add Player"):
        if new_name.strip() == "":
            st.error("Player name cannot be empty.")
        elif new_name in df["name"].tolist():
            st.error("This player already exists.")
        else:
            new_row = {"name": new_name}
            new_row.update(new_stats)
            df = df.append(new_row, ignore_index=True)
            df.to_csv("players.csv", index=False)
            st.success(f"{new_name} added successfully!")
