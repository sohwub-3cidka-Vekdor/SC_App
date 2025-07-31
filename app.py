import streamlit as st
import pandas as pd
import random
import os

# Load or initialize player data
DATA_FILE = "players.csv"
if os.path.exists(DATA_FILE):
    players_df = pd.read_csv(DATA_FILE)
else:
    players_df = pd.DataFrame(columns=["name", "technicality", "strength", "control", "finish", "stamina"])

st.set_page_config(page_title="SC Brésil - Team Creator", layout="wide")

# --- Sidebar Navigation ---
page = st.sidebar.selectbox("Choose a page", ["Team Creator", "Edit Players"])

# --- Shared Functions ---
def calculate_team_score(team, df):
    stats = [tTechnicality", "strength", "control", "finish", "stamina"]
    team_df = df[df["name"].isin(team)]  # Ensure column name matches
    return team_df[stats].sum().sum()

def generate_team_combinations(players):
    n = len(players)
    if n < 2:
        return []

    combinations = []
    if n == 2:
        combinations.append([players[:1], players[1:]])
    elif n == 3:
        combinations.append([players[:2], players[2:]])
    elif n == 4:
        combinations.append([players[:2], players[2:]])
    elif n == 5:
        combinations.append([players[:3], players[3:]])
    elif n % 2 == 0:
        combinations.append([players[:n//2], players[n//2:]])
    elif n % 3 == 0:
        third = n // 3
        combinations.append([players[:third], players[third:2*third], players[2*third:]])
    elif n >= 6:
        a = n // 3
        combinations.append([players[:a], players[a:2*a], players[2*a:]])
    return combinations

def find_best_teams(selected_players, df):
    best_combination = None
    min_diff = float("inf")
    combinations = generate_team_combinations(selected_players)
    for teams in combinations:
        scores = [calculate_team_score(team, df) for team in teams]
        diff = max(scores) - min(scores)
        if diff < min_diff:
            min_diff = diff
            best_combination = teams
    return best_combination

# --- Team Creator Page ---
if page == "Team Creator":
    st.title("⚽ SC Brésil - Team Creator")
    st.subheader("✅ Select today's players:")

    players = players_df["Name"].tolist()  # Ensure column name matches
    if "selected_players" not in st.session_state:
        st.session_state.selected_players = []

    # Mobile-friendly layout: display buttons in 3 columns
    num_cols = 3
    cols = st.columns(num_cols)
    for i, player in enumerate(players):
        with cols[i % num_cols]:
            if player in st.session_state.selected_players:
                if st.button(f"✅ {player}", key=player):
                    st.session_state.selected_players.remove(player)
            else:
                if st.button(player, key=player):
                    st.session_state.selected_players.append(player)

    st.markdown("---")

    if st.button("🎲 Generate Teams") and len(st.session_state.selected_players) >= 2:
        best_teams = find_best_teams(st.session_state.selected_players, players_df)
        if best_teams:
            for i, team in enumerate(best_teams, start=1):
                st.subheader(f"Team {i}")
                st.write(team)
    elif len(st.session_state.selected_players) < 2:
        st.warning("Please select at least 2 players.")

# --- Edit Players Page ---
elif page == "Edit Players":
    st.title("✏️ Edit Player Stats")

    name_list = players_df["Name"].tolist()  # Ensure column name matches
    selected = st.selectbox("Select a player to edit or add a new name below:", [""] + name_list)
    new_name = st.text_input("New Player Name:", "" if selected else "")

    if selected:
        player_data = players_df[players_df["Name"] == selected].iloc[0]
    else:
        player_data = pd.Series({"Technicality": 3, "Strength": 3, "Control": 3, "Finish": 3, "Stamina": 3})

    technicality = st.slider("Technicality", 1, 5, int(player_data["Technicality"]))
    strength = st.slider("Strength", 1, 5, int(player_data["Strength"]))
    control = st.slider("Control", 1, 5, int(player_data["Control"]))
    finish = st.slider("Finish", 1, 5, int(player_data["Finish"]))
    stamina = st.slider("Stamina", 1, 5, int(player_data["Stamina"]))

    if st.button("💾 Save Player"):
        name = selected if selected else new_name
        if not name:
            st.error("Please enter a name.")
        else:
            new_entry = pd.DataFrame([{
                "Name": name,  # Ensure column name matches
                "Technicality": technicality,
                "Strength": strength,
                "Control": control,
                "Finish": finish,
                "Stamina": stamina
            }])
            players_df = players_df[players_df["Name"] != name]  # Ensure column name matches
            players_df = pd.concat([players_df, new_entry], ignore_index=True)
            players_df.to_csv(DATA_FILE, index=False)
            st.success(f"Stats saved for {name} ✅")

    st.markdown("---")
    if st.checkbox("📋 Show current player data"):
        st.dataframe(players_df)
