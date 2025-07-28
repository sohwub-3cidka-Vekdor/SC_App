# 📦 Imports
import streamlit as st
import pandas as pd
import numpy as np
from itertools import combinations

# ✅ Paste this below your imports 👇
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

    # Try 3-team splits (only if enough players)
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

# 📌 3. Start the Streamlit app UI
st.title("⚽ SC Brésil - Team Creator")

df = pd.read_csv("players.csv")

selected_players = st.multiselect(
    "✅ Select today's players:",
    df["name"].tolist()
)

selected_df = df[df["name"].isin(selected_players)]

if not selected_df.empty:
    st.subheader("🧍 Selected Players")
    st.dataframe(selected_df)

    if st.button("Create Balanced Teams"):
        if len(selected_players) < 2:
            st.warning("Select at least 2 players.")
        else:
            best_teams, balance_score = balance_any_number_of_players(selected_df)

            if best_teams is None:
                st.error("❌ No valid team split found.")
            else:
                st.success(f"✅ Best match found! Balance Score: {round(balance_score)}")

                cols = st.columns(len(best_teams))

                for i, team in enumerate(best_teams):
                    with cols[i]:
                        st.subheader(f"Team {i+1} ({len(team)} players)")
                        st.write(selected_df[selected_df["name"].isin(team)])
else:
    st.info("Please select at least 2 players to form teams.")
