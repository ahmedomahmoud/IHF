from orm import Team, Championship, TeamInChamp, Player, Match, Referee, RefereeInMatch, PlayerStats
from parser import parse_cp_file
from pprint import pprint

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Date,
    ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv
from datetime import date
import json

parsed_data = parse_cp_file("cp-files/txt/01.CP")
pprint(parsed_data["gameinfo"])

load_dotenv()

# Build DATABASE_URL
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    raise RuntimeError("Missing DB configuration in .env")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return -1

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return -1.0

def add_championship(session):
    # Dummy data
    championship_data = {
        "name": "IHF Men's World Championship 2025",
        "description": "The 2025 edition of the International Handball Federation's World Championship.",
        "start_date": date(2025, 1, 13),
        "end_date": date(2025, 1, 31)
    }

    # Check if it already exists
    existing = session.query(Championship).filter_by(name=championship_data["name"]).first()
    if existing:
        print(f"Championship already exists: {existing}")
        return existing

    # Create and add
    championship = Championship(**championship_data)
    session.add(championship)
    session.commit()
    print(f"Added championship: {championship}")
    return championship

def create_teams(parsed_data, session):
   
    gameinfo = parsed_data["gameinfo"][0]

    teams_data = [
        {"name": gameinfo["TeamNameA"], "abbreviation": gameinfo["TIDA"]},
        {"name": gameinfo["TeamNameB"], "abbreviation": gameinfo["TIDB"]}
    ]

    for team_data in teams_data:
        existing_team = session.query(Team).filter_by(abbreviation=team_data["abbreviation"]).first()
        if existing_team:
            print(f"Team already exists: {existing_team}")
        else:
            team = Team(**team_data)
            session.add(team)
            print(f"Created new team: {team}")

    session.commit()

def link_team_to_championship(champ_name, team_abbr, session):
  
    championship = session.query(Championship).filter_by(name=champ_name).first()
    if not championship:
        raise ValueError(f"Championship with name '{champ_name}' not found.")

    team = session.query(Team).filter_by(abbreviation=team_abbr).first()
    if not team:
        raise ValueError(f"Team with abbreviation '{team_abbr}' not found.")

    existing_link = session.query(TeamInChamp).filter_by(
        team_id=team.id,
        championship_id=championship.id
    ).first()

    if existing_link:
        print(f"Link already exists: Team {team_abbr} in {champ_name}")
    else:
        link = TeamInChamp(team_id=team.id, championship_id=championship.id)
        session.add(link)
        session.commit()
        print(f"Linked team {team_abbr} to championship {champ_name}")

def add_match(parsed_data, session, championship_name):
    gameinfo = parsed_data["gameinfo"][0]

    # Extract game basic info
    game_code = gameinfo["Game"]
    status = gameinfo.get("GStatus")

    # Get team abbreviations
    team_a_abbr = gameinfo["TIDA"]
    team_b_abbr = gameinfo["TIDB"]

    # Get team scores
    team_a_score = {
        "total": safe_int(gameinfo["RA"]) ,
        "first_half": safe_int(gameinfo["RA1"]) ,
        "second_half": safe_int(gameinfo["RA2"]) 
    }

    team_b_score = {
        "total": safe_int(gameinfo["RB"]),
        "first_half": safe_int(gameinfo["RB1"]) ,
        "second_half": safe_int(gameinfo["RB2"]) 
    }

    # Resolve IDs
    championship = session.query(Championship).filter_by(name=championship_name).first()
    if not championship:
        raise ValueError(f"Championship '{championship_name}' not found.")

    team_a = session.query(Team).filter_by(abbreviation=team_a_abbr).first()
    if not team_a:
        raise ValueError(f"Team '{team_a_abbr}' not found.")

    team_b = session.query(Team).filter_by(abbreviation=team_b_abbr).first()
    if not team_b:
        raise ValueError(f"Team '{team_b_abbr}' not found.")

    # Check if match already exists
    existing_match = session.query(Match).filter_by(game_code=game_code).first()
    if existing_match:
        print(f"Match with code '{game_code}' already exists.")
        return existing_match

    # Create match object
    match = Match(
        game_code=game_code,
        championship_id=championship.id,
        team_a_id=team_a.id,
        team_b_id=team_b.id,
        team_a_score=team_a_score,
        team_b_score=team_b_score,
        status=status
    )

    session.add(match)
    session.commit()
    print(f"Match added: {match}")
    return match

def clean_stats(row):
    return {
        "all_goals": safe_int(row.get("AllG")),
        "all_shots": safe_int(row.get("AllShots")),
        "all_efficiency": safe_float(row.get("AllEff")),
        "goals_7m": safe_int(row.get("P7mG")),
        "eff_7m": safe_float(row.get("P7mEff")),
        "goals_9m": safe_int(row.get("P9mG")),
        "eff_9m": safe_float(row.get("P9mEff")),
        "goals_6m": safe_int(row.get("P6mG")),
        "eff_6m": safe_float(row.get("P6mEff")),
        "goals_near": safe_int(row.get("NearG")),
        "eff_near": safe_float(row.get("NearEff")),
        "goals_wing": safe_int(row.get("WingG")),
        "eff_wing": safe_float(row.get("WingEff")),
        "goals_fastbreak": safe_int(row.get("FBG")),
        "eff_fastbreak": safe_float(row.get("FBEff")),
        "yellow_cards": safe_int(row.get("YC")),
        "red_cards": safe_int(row.get("RC")),
        "blue_cards": safe_int(row.get("EX")),
        "suspensions_2min": safe_int(row.get("P2minT")),
        "total_7m_shots": safe_int(row.get("P7mShots")),
    }

def update_match_stats(parsed_data, session, match_code):
    match = session.query(Match).filter_by(game_code=match_code).first()
    if not match:
        raise ValueError(f"No match found with code {match_code}")

    statteam = parsed_data.get("statteam", [])

    if not statteam or len(statteam) < 2:
        raise ValueError("Statteam data incomplete or missing")

    # Create a mapping from team code to team_id
    team_code_to_stats = {}
    for row in statteam:
        team_code = row.get("Team")
        stats = clean_stats(row)
        team_code_to_stats[team_code] = stats

    # Load actual teams from DB for this match
    team_a = match.team_a
    team_b = match.team_b

    # If teams don't exist (deleted or null), skip setting stats
    if not team_a or not team_b:
        print(f"Match {match_code}: team_a or team_b is None. Skipping stats update.")
        return
    #print(team_code_to_stats)
    # Make sure the teams exist in parsed data
    if team_a.abbreviation not in team_code_to_stats or team_b.abbreviation not in team_code_to_stats:
        print(f"Match {match_code}: One of the teams not found in statteam. Skipping stats update.")
        return
    
    match.team_a_stats = team_code_to_stats[team_a.abbreviation]
    match.team_b_stats = team_code_to_stats[team_b.abbreviation]

    session.commit()

def insert_referees(parsed_data, session):
    referee_data = parsed_data.get("referee", [])
    if not referee_data:
        print("No referee data found.")
        return

    referee_entry = referee_data[0]
    game_code = referee_entry.get("Game")

    match = session.query(Match).filter_by(game_code=game_code).first()
    if not match:
        print(f"No match found for game code: {game_code}")
        return

    referees = [
        {
            "name": referee_entry.get("Name1", ""),
            "country": referee_entry.get("Nat1", ""),
            "role": referee_entry.get("REF1Kind", "")
        },
        {
            "name": referee_entry.get("Name2", ""),
            "country": referee_entry.get("Nat2", ""),
            "role": referee_entry.get("REF2Kind", "")
        },
        {
            "name": referee_entry.get("Name3", ""),
            "country": referee_entry.get("Nat3", ""),
            "role": referee_entry.get("REF3Kind", "")
        }
    ]

    for ref in referees:
        if not ref["name"]:
            continue  # Skip empty referee

        # Check if referee exists
        existing_ref = session.query(Referee).filter_by(
            name=ref["name"],
            country=ref["country"]
        ).first()

        if not existing_ref:
            existing_ref = Referee(
                name=ref["name"],
                country=ref["country"]
            )
            session.add(existing_ref)
            session.flush()

        # Check if already linked to match to avoid duplicates
        existing_link = session.query(RefereeInMatch).filter_by(
            match_id=match.id,
            referee_id=existing_ref.id,
            role=ref["role"]
        ).first()

        if not existing_link:
            match_ref_link = RefereeInMatch(
                match_id=match.id,
                referee_id=existing_ref.id,
                role=ref["role"]
            )
            session.add(match_ref_link)

    session.commit()



def insert_players(parsed_data,  session):
    statind = parsed_data.get("statind", [])

    if not statind:
        print("No player data found in [statind].")
        return

    for row in statind:
        first_name = row.get("FirstName")
        last_name = row.get("SurName")
        number = row.get("Nr")
        team_abbr = row.get("TID")

        if not (first_name and last_name and team_abbr):
            continue

        # Find team
        team = session.query(Team).filter_by(abbreviation=team_abbr).first()
        if not team:
            print(f"Team '{team_abbr}' not found for player {first_name} {last_name}")
            continue

        # Check if player exists
        existing_player = session.query(Player).filter_by(
            first_name=first_name,
            last_name=last_name,
            team_id=team.id
        ).first()

        if existing_player:
            print(f"Player {first_name} {last_name} already exists.")
        else:
            new_player = Player(
                first_name=first_name,
                last_name=last_name,
                number=safe_int(number) ,
                team_id=team.id
            )
            session.add(new_player)
            print(f"Inserted player {first_name} {last_name} (Team: {team_abbr})")

    session.commit()



def insert_player_stats(parsed_data, session):
    

    statind = parsed_data.get("statind", [])
    gameinfo = parsed_data.get("gameinfo", [])

    if not statind or not gameinfo:
        print("Missing [statind] or [gameinfo] section.")
        return

    game_code = gameinfo[0]["Game"]
    match = session.query(Match).filter_by(game_code=game_code).first()

    if not match:
        print(f"Match {game_code} not found.")
        return

    for row in statind:
        first_name = row.get("FirstName")
        last_name = row.get("SurName")
        team_abbr = row.get("TID")

        if not (first_name and last_name and team_abbr):
            continue

        team = session.query(Team).filter_by(abbreviation=team_abbr).first()
        if not team:
            print(f"Team {team_abbr} not found.")
            continue

        player = session.query(Player).filter_by(
            first_name=first_name,
            last_name=last_name,
            team_id=team.id
        ).first()

        if not player:
            print(f"Player {first_name} {last_name} not found in team {team_abbr}")
            continue

        # Check if stats already exist
        existing = session.query(PlayerStats).filter_by(
            match_id=match.id,
            player_id=player.id
        ).first()

        if existing:
            print(f"Stats already exist for {first_name} {last_name} in match {game_code}")
            continue

        stats_json = {
            "all_goals": safe_int(row.get("AllG")),
            "shots_efficiency": safe_float(row.get("AllEff")),
            "yellow_cards": safe_int(row.get("YC")),
            "red_cards": safe_int(row.get("RC")),
            "blue_cards": safe_int(row.get("EX")),
            "suspensions_2min": safe_int(row.get("P2minT"))
        }

        player_stats = PlayerStats(
            match_id=match.id,
            player_id=player.id,
            team_id=team.id,
            stats=stats_json
        )

        session.add(player_stats)
        print(f"Inserted stats for {first_name} {last_name} (match {game_code})")

    session.commit()

if __name__ == "__main__":
    session = SessionLocal()
    try:
        # Step 1: Create teams from parsed_data
        add_championship(session)
        create_teams(parsed_data, session)

        # Step 2: Link each team to the championship by name
        link_team_to_championship("IHF Men's World Championship 2025", "AUT", session)
        link_team_to_championship("IHF Men's World Championship 2025", "ARG", session)
        match = add_match(parsed_data, session, "IHF Men's World Championship 2025")
        update_match_stats(parsed_data, session, match.game_code)
        insert_referees(parsed_data,  session)
        insert_players(parsed_data, session)
        insert_player_stats(parsed_data, session)
    finally:
        session.close()
