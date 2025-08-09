from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import schemas
import utils
import auth
import database
from fastapi.security import OAuth2PasswordRequestForm
from manage_data.parser import parse_cp_file
from manage_data.data_orm import Champ
from manage_data.orm import SessionLocal, Team, Championship, Match, Player, RefereeInMatch, PlayerStats
from sqlalchemy.orm import Session
from pprint import pprint
from datetime import date

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- REGISTER ---
@app.post("/auth/register", status_code=201)
async def register(user: schemas.UserCreate):
    existing_user = await database.user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = utils.hash_password(user.password)

    new_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "password": hashed_pw
    }

    result = await database.user_collection.insert_one(new_user)

    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}


# --- LOGIN ---
@app.post("/auth/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await database.user_collection.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not utils.verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = auth.create_access_token(data={"sub": user["username"]})

    return {"access_token": token, "token_type": "bearer"}


# --- UPLOAD CP FILE ---
@app.post("/upload-cp-file/")
async def upload_cp_file(file: UploadFile = File(...), current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    file_content = await file.read()
    parsed_data = parse_cp_file(file_content)
    pprint(parsed_data["gameinfo"])
    try:
        champ = Champ(name="World Handball Championship 2025", session=db)
        if not champ.champ_exists:
            champ.add_championship("World Handball Championship 2025", "The 29th edition of the championship.", date(2025, 1, 14), date(2025, 2, 2))
        print("Processing parsed data...")
        champ.process_data(parsed_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()


# --- Championship Routes ---
@app.get("/championships", response_model=list[schemas.ChampionshipOut])
def get_championships(db: Session = Depends(get_db)):
    return db.query(Championship).all()

@app.get("/championships/{championship_id}", response_model=schemas.ChampionshipOut)
def get_championship_by_id(championship_id: int, db: Session = Depends(get_db)):
    championship = db.query(Championship).filter(Championship.id == championship_id).first()
    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found")
    return championship

@app.get("/championships/name/{championship_name}", response_model=schemas.ChampionshipOut)
def get_championship_by_name(championship_name: str, db: Session = Depends(get_db)):
    championship = db.query(Championship).filter(Championship.name == championship_name).first()
    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found")
    return championship

@app.post("/championships", response_model=schemas.ChampionshipOut, status_code=201)
def create_championship(championship: schemas.ChampionshipCreate, current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_championship = Championship(**championship.dict())
    db.add(new_championship)
    db.commit()
    db.refresh(new_championship)
    return new_championship

# --- Team Routes ---
@app.get("/teams", response_model=list[schemas.TeamOut])
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()

@app.get("/teams/{team_id}", response_model=schemas.TeamOut)
def get_team_by_id(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.get("/teams/abbreviation/{abbreviation}", response_model=schemas.TeamOut)
def get_team_by_abbreviation(abbreviation: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.abbreviation == abbreviation).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.post("/teams", response_model=schemas.TeamOut, status_code=201)
def create_team(team: schemas.TeamCreate, current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    new_team = Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

# --- Match Routes ---
@app.get("/matches/{match_id}/score", response_model=schemas.MatchScoreOut)
def get_match_score(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@app.get("/matches/{match_id}/teams/{team_id}/stats", response_model=schemas.MatchStatesOut)
def get_team_stats_in_match(match_id: int, team_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id, (Match.team_a_id == team_id) | (Match.team_b_id == team_id)).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match or Team not found in this match")
    return match

@app.get("/matches/{match_id}/referees", response_model=list[schemas.RefereeWithRoleOut])
def get_referees_in_match(match_id: int, db: Session = Depends(get_db)):
    referees_in_match = db.query(RefereeInMatch).filter(RefereeInMatch.match_id == match_id).all()
    if not referees_in_match:
        raise HTTPException(status_code=404, detail="Referees not found for this match")

    response = []
    for ref_in_match in referees_in_match:
        response.append(
            schemas.RefereeWithRoleOut(
                id=ref_in_match.referee.id,
                name=ref_in_match.referee.name,
                country=ref_in_match.referee.country,
                role=ref_in_match.role,
            )
        )
    return response

# --- Player Routes ---
@app.get("/teams/{team_id}/players", response_model=list[schemas.PlayerOut])
def get_players_by_team(team_id: int, db: Session = Depends(get_db)):
    players = db.query(Player).filter(Player.team_id == team_id).all()
    if not players:
        raise HTTPException(status_code=404, detail="Players not found for this team")
    return players

@app.get("/matches/{match_id}/teams/{team_id}/players/stats", response_model=list[schemas.PlayerStatsOut])
def get_players_stats_in_match_for_team(match_id: int, team_id: int, db: Session = Depends(get_db)):
    player_stats = db.query(PlayerStats).filter(PlayerStats.match_id == match_id, PlayerStats.team_id == team_id).all()
    if not player_stats:
        raise HTTPException(status_code=404, detail="Player stats not found for this team in this match")
    return player_stats

@app.get("/matches/{match_id}/players/stats", response_model=list[schemas.PlayerStatsOut])
def get_all_player_stats_in_match(match_id: int, db: Session = Depends(get_db)):
    player_stats = db.query(PlayerStats).filter(PlayerStats.match_id == match_id).all()
    if not player_stats:
        raise HTTPException(status_code=404, detail="Player stats not found for this match")
    return player_stats

@app.get("/matches/{match_id}/teams/{team_id}/players/{player_id}/stats", response_model=schemas.PlayerStatsOut)
def get_player_stats_in_match(match_id: int, team_id: int, player_id: int, db: Session = Depends(get_db)):
    player_stats = db.query(PlayerStats).filter(
        PlayerStats.match_id == match_id, 
        PlayerStats.team_id == team_id, 
        PlayerStats.player_id == player_id
    ).first()
    if not player_stats:
        raise HTTPException(status_code=404, detail="Player stats not found for this player in this match")
    return player_stats
