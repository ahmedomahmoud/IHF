from parser import parse_cp_file
from pprint import pprint
import psycopg2
from dotenv import load_dotenv
import os
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


def insert_match(parsed_data, conn):
    gameinfo = parsed_data["gameinfo"][0]

    game_code = gameinfo["Game"]
    team_a_abbr = gameinfo["TIDA"]
    team_b_abbr = gameinfo["TIDB"]

    # Step 1: Look up team_a_id and team_b_id from abbreviation
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_a_abbr,))
        team_a_row = cur.fetchone()
        if not team_a_row:
            print(f"Team A with abbreviation {team_a_abbr} not found.")
            return
        team_a_id = team_a_row[0]

        cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_b_abbr,))
        team_b_row = cur.fetchone()
        if not team_b_row:
            print(f"Team B with abbreviation {team_b_abbr} not found.")
            return
        team_b_id = team_b_row[0]

        # Step 2: Prepare match data
        match_data = {
            "game_code": game_code,
            "championship_id": championship_id,
            "team_a_id": team_a_id,
            "team_b_id": team_b_id,
            "score_a": int(gameinfo["RA"]) if gameinfo["RA"] else None,
            "score_b": int(gameinfo["RB"]) if gameinfo["RB"] else None,
            "score_a_1st_half": int(gameinfo["RA1"]) if gameinfo["RA1"] else None,
            "score_b_1st_half": int(gameinfo["RB1"]) if gameinfo["RB1"] else None,
            "score_a_2nd_half": int(gameinfo["RA2"]) if gameinfo["RA2"] else None,
            "score_b_2nd_half": int(gameinfo["RB2"]) if gameinfo["RB2"] else None,
            "status": gameinfo["GStatus"] or None,
        }

        # Step 3: Check if match already exists
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        if cur.fetchone():
            print(f"Match with game_code {game_code} already exists. Skipping insert.")
        else:
            cur.execute("""
                INSERT INTO matches (
                    game_code, championship_id,
                    team_a_id, team_b_id,
                    score_a, score_b,
                    score_a_1st_half, score_b_1st_half,
                    score_a_2nd_half, score_b_2nd_half,
                    status
                ) VALUES (
                    %(game_code)s, %(championship_id)s,
                    %(team_a_id)s, %(team_b_id)s,
                    %(score_a)s, %(score_b)s,
                    %(score_a_1st_half)s, %(score_b_1st_half)s,
                    %(score_a_2nd_half)s, %(score_b_2nd_half)s,
                    %(status)s
                )
            """, match_data)
            print(f"Inserted match {game_code} between {team_a_abbr} and {team_b_abbr}")

        conn.commit()

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
            print(f" Match {game_code} not found.")
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

            def parse_int(val): return int(val) if val and val.isdigit() else 0
            def parse_float(val): 
                try: return float(val)
                except: return 0.0

            stats = {
                "match_id": match_id,
                "player_id": player_id,
                "team_id": team_id,
                "all_goals": parse_int(row.get("AllG")),
                "shots_efficiency": parse_float(row.get("AllEff")),
                "yellow_cards": parse_int(row.get("YC")),
                "red_cards": parse_int(row.get("RC")),
                "blue_cards": parse_int(row.get("EX")),
                "suspensions_2min": parse_int(row.get("P2minT"))
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
                    match_id, player_id, team_id,
                    all_goals, shots_efficiency,
                    yellow_cards, red_cards, blue_cards, suspensions_2min
                ) VALUES (
                    %(match_id)s, %(player_id)s, %(team_id)s,
                    %(all_goals)s, %(shots_efficiency)s,
                    %(yellow_cards)s, %(red_cards)s, %(blue_cards)s, %(suspensions_2min)s
                )
            """, stats)
            print(f"Inserted stats for {first_name} {last_name} (match {game_code})")

        conn.commit()

def insert_team_stats(parsed_data, conn):
    statteam = parsed_data.get("statteam", [])
    gameinfo = parsed_data.get("gameinfo", [])

    if not statteam or not gameinfo:
        print("Missing [statteam] or [gameinfo] section.")
        return

    game_code = gameinfo[0]["Game"]

    with conn.cursor() as cur:
        # Get match_id
        cur.execute("SELECT id FROM matches WHERE game_code = %s", (game_code,))
        match = cur.fetchone()
        if not match:
            print(f"Match {game_code} not found.")
            return

        match_id = match[0]

        for row in statteam:
            team_abbr = row.get("TID")
            if not team_abbr:
                continue

            # Get team_id
            cur.execute("SELECT id FROM teams WHERE abbreviation = %s", (team_abbr,))
            team = cur.fetchone()
            if not team:
                print(f"Team {team_abbr} not found.")
                continue

            team_id = team[0]

            # Check if stats already inserted
            cur.execute("""
                SELECT 1 FROM team_stats
                WHERE match_id = %s AND team_id = %s
            """, (match_id, team_id))

            if cur.fetchone():
                print(f"Team stats already exist for team {team_abbr} in match {game_code}")
                continue

            def parse_int(val): return int(val) if val and val.isdigit() else 0
            def parse_float(val): 
                try: return float(val)
                except: return 0.0

            stats = {
                "match_id": match_id,
                "team_id": team_id,
                "all_goals": parse_int(row.get("AllG")),
                "all_shots": parse_int(row.get("AllShots")),
                "all_efficiency": parse_float(row.get("AllEff")),
                "goals_7m": parse_int(row.get("P7mG")),
                "eff_7m": parse_float(row.get("P7mEff")),
                "goals_9m": parse_int(row.get("P9mG")),
                "eff_9m": parse_float(row.get("P9mEff")),
                "goals_6m": parse_int(row.get("P6mG")),
                "eff_6m": parse_float(row.get("P6mEff")),
                "goals_near": parse_int(row.get("NearG")),
                "eff_near": parse_float(row.get("NearEff")),
                "goals_wing": parse_int(row.get("WingG")),
                "eff_wing": parse_float(row.get("WingEff")),
                "goals_fastbreak": parse_int(row.get("FBG")),
                "eff_fastbreak": parse_float(row.get("FBEff")),
                "yellow_cards": parse_int(row.get("YC")),
                "red_cards": parse_int(row.get("RC")),
                "blue_cards": parse_int(row.get("EX")),
                "suspensions_2min": parse_int(row.get("P2minT")),
                "total_7m_shots": parse_int(row.get("P7mShots"))
            }

            cur.execute("""
                INSERT INTO team_stats (
                    match_id, team_id,
                    all_goals, all_shots, all_efficiency,
                    goals_7m, eff_7m,
                    goals_9m, eff_9m,
                    goals_6m, eff_6m,
                    goals_near, eff_near,
                    goals_wing, eff_wing,
                    goals_fastbreak, eff_fastbreak,
                    yellow_cards, red_cards, blue_cards,
                    suspensions_2min, total_7m_shots
                ) VALUES (
                    %(match_id)s, %(team_id)s,
                    %(all_goals)s, %(all_shots)s, %(all_efficiency)s,
                    %(goals_7m)s, %(eff_7m)s,
                    %(goals_9m)s, %(eff_9m)s,
                    %(goals_6m)s, %(eff_6m)s,
                    %(goals_near)s, %(eff_near)s,
                    %(goals_wing)s, %(eff_wing)s,
                    %(goals_fastbreak)s, %(eff_fastbreak)s,
                    %(yellow_cards)s, %(red_cards)s, %(blue_cards)s,
                    %(suspensions_2min)s, %(total_7m_shots)s
                )
            """, stats)

            print(f"Inserted team stats for team {team_abbr} (match {game_code})")

        conn.commit()

insert_teams(data, conn)
insert_match(data, conn)
insert_referees(data, conn)
insert_players(data, conn)
insert_player_stats(data, conn)
insert_team_stats(data, conn)
# Done
conn.close()
