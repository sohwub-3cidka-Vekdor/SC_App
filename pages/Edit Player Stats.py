import streamlit as st
import pandas as pd
import os

st.title("📝 Edit or Add Player Stats")

# Load data
if os.path.exists("players.csv"):
    df = pd.read_csv("players.csv")
else:
    df = pd.DataFrame(columns=["name", "tech", "strength", "control", "finish", "stamina"])

# Tabs
tab1, tab2, tab3 = st.tabs(["✏️ Edit Player", "➕ Add New Player", "🔥 Delete Player"])

with tab1:
    if df.empty:
        st.warning("No players found. Please add new players first.")
    else:
        # Select player to edit
        selected_player = st.selectbox("Select a player to edit:", df["name"].tolist())
        player_data = df[df["name"] == selected_player].iloc[0]

        # Editable name
        new_name = st.text_input("Change Player Name", value=selected_player, key="edit_name")

        updated_stats = {}
        for col in df.columns[1:]:
            updated_stats[col] = st.slider(
                f"{col.capitalize()}", 1, 5, int(player_data[col]), key=f"edit_{col}"
            )

        if st.button("💾 Save Changes"):
            # Check for name conflict if renaming
            if new_name != selected_player and new_name in df["name"].values:
                st.error("⚠️ Another player with this name already exists.")
            elif new_name.strip() == "":
                st.error("⚠️ Player name cannot be empty.")
            else:
                df.loc[df["name"] == selected_player, "name"] = new_name
                for stat, value in updated_stats.items():
                    df.loc[df["name"] == new_name, stat] = value
                df.to_csv("players.csv", index=False)
                st.success(f"✅ {new_name}'s stats updated!")
                st.experimental_rerun()

with tab2:
    if df.empty:
        st.warning("No players to delete.")
    else:
        player_to_delete = st.selectbox("Select a player to delete:", df["name"].tolist())
        if st.button("🗑️ Delete Player"):
            df = df[df["name"] != player_to_delete]
            df.to_csv("players.csv", index=False)
            st.success(f"🗑️ Deleted {player_to_delete}.")
            st.experimental_rerun()