from parser import parse_cp_file
from pprint import pprint
import psycopg2
from dotenv import load_dotenv
import os
import json
championship_id=1

data = parse_cp_file("cp-files/txt/01.CP")
pprint(data["gameinfo"])

load_dotenv()

# Get DB credentials from .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")

# Create DB connection
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
def insert_teams(parsed_data, conn, championship_id=1):
    gameinfo = parsed_data['gameinfo'][0]

    teams = [
        {
            "name": gameinfo["TeamNameA"],
            "abbreviation": gameinfo["TIDA"]
        },
        {
            "name": gameinfo["TeamNameB"],
            "abbreviation": gameinfo["TIDB"]
        }
    ]

    with conn.cursor() as cur:
        for team in teams:
            # Step 1: Check if team exists by abbreviation
            cur.execute("""
                SELECT id FROM teams
                WHERE abbreviation = %(abbreviation)s
            """, team)

            result = cur.fetchone()

            if result:
                team_id = result[0]
                print(f"Team '{team['name']}' already exists — ID: {team_id}")
            else:
                # Insert new team
                cur.execute("""
                    INSERT INTO teams (name, abbreviation)
                    VALUES (%(name)s, %(abbreviation)s)
                    RETURNING id
                """, team)
                team_id = cur.fetchone()[0]
                print(f"Inserted team: {team['name']} ({team['abbreviation']}) — ID: {team_id}")

            # Step 2: Insert into team_part_champ if not already linked
            cur.execute("""
                SELECT 1 FROM team_in_champ
                WHERE team_id = %s AND championship_id = %s
            """, (team_id, championship_id))

            already_linked = cur.fetchone()

            if not already_linked:
                cur.execute("""
                    INSERT INTO team_in_champ (team_id, championship_id)
                    VALUES (%s, %s)
                """, (team_id, championship_id))
                print(f"Linked team ID {team_id} to championship {championship_id}")
            else:
                print(f"Team ID {team_id} is already linked to championship {championship_id}")

        conn.commit()


def extract_score_json(team_data):
    return {
        "total": int(team_data["G"]),         # Goals
        "first_half": int(team_data["G1"]),   # First half goals
        "second_half": int(team_data["G2"])   # Second half goals
    }


def insert_match(parsed_data, conn):
    gameinfo = parsed_data["gameinfo"][0]

    game_code = gameinfo["Game"]
    team_a_abbr = gameinfo["TIDA"]
    team_b_abbr = gameinfo["TIDB"]

    with conn.cursor() as cur:
        # Get team A ID
        cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_a_abbr,))
        team_a_row = cur.fetchone()
        if not team_a_row:
            print(f"Team A with abbreviation {team_a_abbr} not found.")
            return None
        team_a_id = team_a_row[0]

        # Get team B ID
        cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_b_abbr,))
        team_b_row = cur.fetchone()
        if not team_b_row:
            print(f"Team B with abbreviation {team_b_abbr} not found.")
            return None
        team_b_id = team_b_row[0]

        # Check if match already exists
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        existing = cur.fetchone()
        if existing:
            print(f"Match with game_code {game_code} already exists. Skipping insert.")
            return existing[0]  # Return existing match_id

        # Build score JSONs
        team_a_score = {
            "total": int(gameinfo["RA"]) if gameinfo["RA"] else 0,
            "first_half": int(gameinfo["RA1"]) if gameinfo["RA1"] else 0,
            "second_half": int(gameinfo["RA2"]) if gameinfo["RA2"] else 0
        }

        team_b_score = {
            "total": int(gameinfo["RB"]) if gameinfo["RB"] else 0,
            "first_half": int(gameinfo["RB1"]) if gameinfo["RB1"] else 0,
            "second_half": int(gameinfo["RB2"]) if gameinfo["RB2"] else 0
        }

        # Prepare data for insertion
        match_data = {
            "game_code": game_code,
            "championship_id": championship_id,
            "team_a_id": team_a_id,
            "team_b_id": team_b_id,
            "team_a_score": json.dumps(team_a_score),
            "team_b_score": json.dumps(team_b_score),
            "status": gameinfo.get("GStatus")
        }

        # Insert into matches table
        cur.execute("""
            INSERT INTO matches (
                game_code, championship_id,
                team_a_id, team_b_id,
                team_a_score, team_b_score,
                status
            ) VALUES (
                %(game_code)s, %(championship_id)s,
                %(team_a_id)s, %(team_b_id)s,
                %(team_a_score)s, %(team_b_score)s,
                %(status)s
            ) RETURNING id
        """, match_data)

        match_id = cur.fetchone()[0]
        conn.commit()
        print(f"Inserted match {game_code} between {team_a_abbr} and {team_b_abbr}")
        return match_id


def insert_referees(parsed_data, conn):
    referee_data = parsed_data.get("referee", [])
    gameinfo_data = parsed_data.get("gameinfo", [])

    if not referee_data or not gameinfo_data:
        print("No referee or gameinfo data found in the parsed file.")
        return

    game_code = gameinfo_data[0]["Game"]

    # Step 1: Get match ID using game_code
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        match = cur.fetchone()

        if not match:
            print(f"Match with game_code {game_code} not found. Can't insert referees.")
            return

        match_id = match[0]

        # Step 2: Build referee list from parsed data
        referee_entry = referee_data[0]  # one row per match
        referees = [
            {
                "name": referee_entry["Name1"],
                "country": referee_entry["Nat1"],
                "role": referee_entry["REF1Kind"]
            },
            {
                "name": referee_entry["Name2"],
                "country": referee_entry["Nat2"],
                "role": referee_entry["REF2Kind"]
            },
            {
                "name": referee_entry["Name3"],
                "country": referee_entry["Nat3"],
                "role": referee_entry["REF3Kind"]
            }
        ]

        for ref in referees:
            if not ref["name"] or not ref["role"]:
                continue  # skip empty entries

            # Step 3: Check if referee exists
            cur.execute("""
                SELECT id FROM referees
                WHERE name = %s AND country = %s
            """, (ref["name"], ref["country"]))
            result = cur.fetchone()

            if result:
                referee_id = result[0]
                print(f"Referee '{ref['name']}' already exists — ID: {referee_id}")
            else:
                # Insert referee
                cur.execute("""
                    INSERT INTO referees (name, country)
                    VALUES (%s, %s)
                    RETURNING id
                """, (ref["name"], ref["country"]))
                referee_id = cur.fetchone()[0]
                print(f"Inserted referee: {ref['name']} ({ref['country']}) — ID: {referee_id}")

            # Step 4: Link referee to match
            cur.execute("""
                SELECT 1 FROM referee_in_match
                WHERE match_id = %s AND referee_id = %s
            """, (match_id, referee_id))

            if cur.fetchone():
                print(f"Referee {ref['name']} already linked to match {game_code}.")
            else:
                cur.execute("""
                    INSERT INTO referee_in_match (match_id, referee_id, role)
                    VALUES (%s, %s, %s)
                """, (match_id, referee_id, ref["role"]))
                print(f"Linked referee {ref['name']} to match {game_code} as {ref['role']}")

        conn.commit()

def insert_players(parsed_data, conn):
    statind = parsed_data.get("statind", [])

    if not statind:
        print("No player data found in [statind].")
        return

    with conn.cursor() as cur:
        for row in statind:
            first_name = row.get("FirstName")
            last_name = row.get("SurName")
            number = row.get("Nr")
            team_abbr = row.get("TID")

            if not (first_name and last_name and team_abbr):
                continue

            # Get team ID
            cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_abbr,))
            result = cur.fetchone()
            if not result:
                print(f"Team '{team_abbr}' not found for player {first_name} {last_name}")
                continue

            team_id = result[0]

            # Check if player exists
            cur.execute("""
                SELECT id FROM players
                WHERE first_name = %s AND last_name = %s AND team_id = %s
            """, (first_name, last_name, team_id))
            exists = cur.fetchone()

            if exists:
                print(f" Player {first_name} {last_name} already exists.")
            else:
                cur.execute("""
                    INSERT INTO players (first_name, last_name, "Number", team_id)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, number, team_id))
                print(f"Inserted player {first_name} {last_name} (Team: {team_abbr})")

        conn.commit()

def insert_player_stats(parsed_data, conn):

    def safe_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
        
    statind = parsed_data.get("statind", [])
    gameinfo = parsed_data.get("gameinfo", [])

    if not statind or not gameinfo:
        print("Missing [statind] or [gameinfo] section.")
        return

    game_code = gameinfo[0]["Game"]

    with conn.cursor() as cur:
        # Get match ID
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        match = cur.fetchone()
        if not match:
            print(f"Match {game_code} not found.")
            return

        match_id = match[0]

        for row in statind:
            first_name = row.get("FirstName")
            last_name = row.get("SurName")
            team_abbr = row.get("TID")

            if not (first_name and last_name and team_abbr):
                continue

            # Get team ID
            cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_abbr,))
            team = cur.fetchone()
            if not team:
                continue
            team_id = team[0]

            # Get player ID
            cur.execute("""
                SELECT id FROM players
                WHERE first_name = %s AND last_name = %s AND team_id = %s
            """, (first_name, last_name, team_id))
            player = cur.fetchone()
            if not player:
                print(f"Player {first_name} {last_name} not found in team {team_abbr}")
                continue

            player_id = player[0]
            stats_json = {
                "all_goals": safe_int(row.get("AllG")),
                "shots_efficiency": safe_float(row.get("AllEff")),
                "yellow_cards": safe_int(row.get("YC")),
                "red_cards": safe_int(row.get("RC")),
                "blue_cards": safe_int(row.get("EX")),
                "suspensions_2min": safe_int(row.get("P2minT"))
            }


            # Check if already inserted
            cur.execute("""
                SELECT 1 FROM player_stats
                WHERE match_id = %s AND player_id = %s
            """, (match_id, player_id))
            if cur.fetchone():
                print(f"Stats already exist for {first_name} {last_name} in match {game_code}")
                continue

            # Insert stats
            cur.execute("""
                INSERT INTO player_stats (
                    match_id, player_id, team_id, stats
                ) VALUES (%s, %s, %s, %s)
            """, (match_id, player_id, team_id, json.dumps(stats_json)))

            print(f"Inserted stats for {first_name} {last_name} (match {game_code})")

        conn.commit()

def clean_stats(row):

    return {
        "all_goals": int(row["AllG"]),
        "all_shots": int(row["AllShots"]),
        "all_efficiency": float(row["AllEff"]),
        "goals_7m": int(row["P7mG"]),
        "eff_7m": float(row["P7mEff"]),
        "goals_9m": int(row["P9mG"]),
        "eff_9m": float(row["P9mEff"]),
        "goals_6m": int(row["P6mG"]),
        "eff_6m": float(row["P6mEff"]),
        "goals_near": int(row["NearG"]),
        "eff_near": float(row["NearEff"]),
        "goals_wing": int(row["WingG"]),
        "eff_wing": float(row["WingEff"]),
        "goals_fastbreak": int(row["FBG"]),
        "eff_fastbreak": float(row["FBEff"]),
        "yellow_cards": int(row["YC"]),
        "red_cards": int(row["RC"]),
        "blue_cards": int(row["EX"]),
        "suspensions_2min": int(row["P2minT"]),
        "total_7m_shots": int(row["P7mShots"])
    }

def insert_match_team_stats_json(parsed_data, conn):
    statteam = parsed_data.get("statteam", [])
    gameinfo = parsed_data.get("gameinfo", [])

    if not statteam or not gameinfo:
        print("Missing [statteam] or [gameinfo] section.")
        return

    game_code = gameinfo[0]["Game"]

    with conn.cursor() as cur:
        # Get match_id
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        match_row = cur.fetchone()
        if not match_row:
            print(f"Match {game_code} not found.")
            return

        match_id = match_row[0]
        team_a_abbr = gameinfo[0]["TIDA"]
        team_b_abbr = gameinfo[0]["TIDB"]

        team_a_data = next((row for row in statteam if row["TID"] == team_a_abbr), None)
        team_b_data = next((row for row in statteam if row["TID"] == team_b_abbr), None)

        if not team_a_data or not team_b_data:
            print(f"Could not find stats for both teams: {team_a_abbr}, {team_b_abbr}")
            return

        team_a_stats = clean_stats(team_a_data)
        team_b_stats = clean_stats(team_b_data)

        # Update only team stats JSON in matches
        cur.execute("""
            UPDATE matches
            SET team_a_stats = %s,
                team_b_stats = %s
            WHERE id = %s
        """, (
            json.dumps(team_a_stats),
            json.dumps(team_b_stats),
            match_id
        ))

        conn.commit()
        print(f"Updated match {game_code} with team stats JSONs.")
        
insert_teams(data, conn)
insert_match(data, conn)
insert_referees(data, conn)
insert_players(data, conn)
insert_player_stats(data, conn)
insert_match_team_stats_json(data, conn)

# Done
conn.close()
