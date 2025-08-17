from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import schemas
import utils
import auth
from manage_data.parser import CpFileParser
from manage_data.data_orm import Champ
from manage_data.orm import SessionLocal, Team, Championship, Match, Player, RefereeInMatch, PlayerStats , TeamInChamp, User, Action
from sqlalchemy.orm import Session , joinedload

app = FastAPI()
parser = CpFileParser()
# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- REGISTER ---
@app.post("/auth/register", status_code=201, response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = utils.hash_password(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# --- LOGIN ---
@app.post("/auth/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not utils.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# --- UPLOAD CP FILE ---
@app.post("/championships/{championship_id}/upload-cp-file/")
async def upload_cp_file(championship_id: int, file: UploadFile = File(...), current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        champ = Champ(id=championship_id, session=db)
        
        if not champ.champ_exists:
            raise HTTPException(status_code=404, detail=f"Championship '{championship_id}' not found.")
        file_content = await file.read()
        parsed_data = parser.parse(file_content,file.filename)
        champ.process_data(parsed_data)
        
        return {"message": f"File uploaded and processed for championship '{championship_id}' successfully. , new actions count: {len(parsed_data['actions'])}"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {e}")


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

@app.post("/championships", response_model=schemas.ChampionshipOut)
def create_championship(championship: schemas.ChampionshipCreate, current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Championship).filter(Championship.name.ilike(championship.name)).first()
    if existing:
        raise HTTPException(status_code=400,detail=f"Championship '{championship.name}' already exists.")
    new_championship = Championship(**championship.dict())
    db.add(new_championship)
    db.commit()
    db.refresh(new_championship)
    return new_championship

@app.put("/championships/{champ_id}", response_model=schemas.ChampionshipOut)
def update_championship(champ_id: int,updated_champ: schemas.ChampionshipUpdate,current_user: schemas.UserOut = Depends(auth.get_current_user),db: Session = Depends(get_db)):
    # Find the championship
    champ = db.query(Championship).filter(Championship.id == champ_id).first()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")
    # If updating name, check for conflicts
    if updated_champ.name:
        conflict = db.query(Championship).filter(Championship.name.ilike(updated_champ.name),Championship.id != champ_id).first()
        if conflict:
            raise HTTPException(status_code=400,detail=f"Another championship with name '{updated_champ.name}' already exists.")

    # Apply updates only for provided fields
    for field, value in updated_champ.dict(exclude_unset=True).items():
        setattr(champ, field, value)

    # Save changes
    db.commit()
    db.refresh(champ)
    return champ


@app.post("/championships/{champ_id}/teams",response_model=schemas.championshipout_linked,)
def link_teams_to_championship(champ_id: int,team_ids: schemas.TeamIDs,current_user: schemas.UserOut = Depends(auth.get_current_user),db: Session = Depends(get_db)):
    champ = db.query(Championship).filter(Championship.id == champ_id).first()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")
    for team_id in team_ids.team_ids:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found.")
        
        # Prevent duplicate links
        exists = db.query(TeamInChamp).filter_by(
            team_id=team_id, championship_id=champ_id
        ).first()
        if not exists:
            db.add(TeamInChamp(team_id=team_id, championship_id=champ_id))

    champ= db.query(Championship).options(joinedload(Championship.teams)).filter(Championship.id == champ_id).first()

    db.commit()
    return champ

@app.delete("/championships/{champ_id}")
async def delete_championship(champ_id: int,current_user: schemas.UserOut = Depends(auth.get_current_user),db: Session = Depends(get_db)):
    champ = db.query(Championship).filter(Championship.id == champ_id).first()
    if not champ:
        raise HTTPException(status_code=404, detail="Championship not found.")

    db.delete(champ)
    db.commit()

    return {"message": "Championship deleted successfully"}



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

@app.post("/teams", response_model=schemas.TeamOut)
def create_team(team: schemas.TeamCreate, current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    existing_team = db.query(Team).filter((Team.name.ilike(team.name)) | (Team.abbreviation.ilike(team.abbreviation))).first()

    if existing_team:
        raise HTTPException(status_code=400,detail=f"Team with name '{team.name}' or abbreviation '{team.abbreviation}' already exists.")
    new_team = Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@app.put("/teams/{team_id}", response_model=schemas.TeamOut)
def update_team(team_id: int,updated_team: schemas.TeamUpdate,current_user: schemas.UserOut = Depends(auth.get_current_user),db: Session = Depends(get_db)):
    # Fetch team by ID
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    # If updating name or abbreviation, check for conflicts
    if updated_team.name or updated_team.abbreviation:
        conflict = db.query(Team).filter(((Team.name.ilike(updated_team.name)) if updated_team.name else False) |
            ((Team.abbreviation.ilike(updated_team.abbreviation)) if updated_team.abbreviation else False),Team.id != team_id).first()
        if conflict:
            raise HTTPException(status_code=400,detail="Another team already exists with that name or abbreviation.")
    # Apply updates
    for field, value in updated_team.dict(exclude_unset=True).items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)
    return team

@app.delete("/teams/{team_id}",response_model=schemas.TeamOut)
def delete_team(team_id: int ,current_user: schemas.UserOut = Depends(auth.get_current_user),db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    db.delete(team)
    db.commit()
    return team


# --- Match Routes ---

@app.get("/championships/{championship_id}/matches", response_model=list[schemas.MatchBaseOut])
def get_matches_in_championship(championship_id: int, db: Session = Depends(get_db)):
    # First, check if the championship exists to provide a clear error message
    championship = db.query(Championship).filter(Championship.id == championship_id).first()
    if not championship:
        raise HTTPException(status_code=404, detail=f"Championship with id {championship_id} not found.")

    # Query for all matches that have the given championship_id
    matches = db.query(Match).filter(Match.championship_id == championship_id).all()
    
    return matches
@app.get("/matches/{match_id}/score", response_model=schemas.MatchScoreOut)
def get_match_score(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@app.get("/matches/{match_id}/stats", response_model=schemas.MatchStatesOut)
def get_stats_in_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found ")
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

@app.get("/matches/{match_id}/actions/page/{page_no}", response_model= list[schemas.ActionOut])
def get_actions (match_id:int, page_no: int,db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    skip_count = (page_no - 1) * 5
    actions = db.query(Action).filter(Action.match_id == match_id).order_by(Action.data["Time"].desc()).offset(skip_count).limit(5).all()
    return [schemas.ActionOut(**action.data) for action in actions]
