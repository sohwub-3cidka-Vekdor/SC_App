import streamlit as st
import pandas as pd

st.title("Edit Player Stats")

# Load existing data
df = pd.read_csv("players.csv")

# Select player to edit
selected_player = st.selectbox("Select a player to edit:", df["name"].tolist())

# Get the row
player_data = df[df["name"] == selected_player].iloc[0]

# Show sliders to edit stats
updated_stats = {}
for col in df.columns[1:]:
    updated_stats[col] = st.slider(
        f"{col.capitalize()}",
        1, 5, int(player_data[col])
    )

# Save button
if st.button("💾 Save Changes"):
    for stat in updated_stats:
        df.loc[df["name"] == selected_player, stat] = updated_stats[stat]
    df.to_csv("players.csv", index=False)
    st.success(f"Stats for {selected_player} updated!")
