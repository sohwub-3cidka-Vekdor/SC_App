import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations

# Function to balance any number of players into 2 or 3 teams
def balance_any_number_of_players(df):
    players = df["name"].tolist()
    n = len(players)
    player_stats = {p: df[df["name"] == p].iloc[0, 1:].values for p in players}

    best_option = None
    best_diff = float("inf")

    # Try 2-team splits
    for i in range(1, n // 2 + 1):
        for team1 in combinations(players, i):
            team1 = set(team1)
            team2 = set(players) - team1
            if len(team1) == 0 or len(team2) == 0:
                continue

            stats1 = sum(player_stats[p] for p in team1)
            stats2 = sum(player_stats[p] for p in team2)
            diff = np.abs(stats1 - stats2).sum()

            if diff < best_diff:
                best_diff = diff
                best_option = [list(team1), list(team2)]

    # Try 3-team splits
    if n >= 6:
        for i in range(1, n - 1):
            for j in range(1, n - i):
                k = n - i - j
                if k < 1:
                    continue

                for team1 in combinations(players, i):
                    remaining1 = list(set(players) - set(team1))
                    for team2 in combinations(remaining1, j):
                        team3 = list(set(remaining1) - set(team2))
                        team1_stats = sum(player_stats[p] for p in team1)
                        team2_stats = sum(player_stats[p] for p in team2)
                        team3_stats = sum(player_stats[p] for p in team3)

                        diff = (
                            np.abs(team1_stats - team2_stats).sum() +
                            np.abs(team2_stats - team3_stats).sum() +
                            np.abs(team3_stats - team1_stats).sum()
                        )

                        if diff < best_diff:
                            best_diff = diff
                            best_option = [list(team1), list(team2), list(team3)]

    return best_option, best_diff


# === Streamlit App ===
st.set_page_config(page_title="SC Brésil Team Creator", layout="wide")
st.title("⚽ SC Brésil - Team Creator")

# Load player data
df = pd.read_csv("players.csv")
players = df["name"].tolist()

# Initialize session state
if "selected_players" not in st.session_state:
    st.session_state.selected_players = []

st.write("✅ Select today's players:")

# Dynamically set number of columns
if len(players) <= 10:
    num_cols = 3
elif len(players) <= 20:
    num_cols = 4
else:
    num_cols = 5

cols = st.columns(num_cols)

# Display buttons
for i, player in enumerate(players):
    col = cols[i % num_cols]
    if player in st.session_state.selected_players:
        if col.button(f"✅ {player}", key=player):
            st.session_state.selected_players.remove(player)
    else:
        if col.button(player, key=player):
            st.session_state.selected_players.append(player)

# Show selected players
if st.session_state.selected_players:
    st.subheader("🧍 Selected Players")
    selected_df = df[df["name"].isin(st.session_state.selected_players)]
    st.dataframe(selected_df)

    if st.button("Create Balanced Teams"):
        if len(st.session_state.selected_players) < 2:
            st.warning("Select at least 2 players.")
        else:
            best_teams, balance_score = balance_any_number_of_players(selected_df)
            if best_teams is None:
                st.error("❌ No valid team split found.")
            else:
                st.success(f"✅ Best match found! Balance Score: {round(balance_score)}")
                team_cols = st.columns(len(best_teams))
                for i, team in enumerate(best_teams):
                    with team_cols[i]:
                        st.subheader(f"Team {i+1} ({len(team)} players)")
                        st.write(selected_df[selected_df["name"].isin(team)])
else:
    st.info("Please select at least 2 players to form teams.")
