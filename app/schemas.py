from pydantic import BaseModel
from typing import List, Optional,Dict
from datetime import date


# --- User Models ---

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(UserBase):
    id: int


# --- Token Models ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# --- Team Models ---

class TeamBase(BaseModel):
    name: str
    abbreviation: str


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None


class TeamOut(TeamBase):
    id: int


# --- Championship Models ---

class ChampionshipBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date


class ChampionshipCreate(ChampionshipBase):
    pass


class ChampionshipUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ChampionshipOut(ChampionshipBase):
    id: int
    
class championshipout_linked(ChampionshipOut):
    teams: List[TeamOut] = []  # Nested team data

    
class TeamIDs(BaseModel):
    team_ids: List[int]

class PlayerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    number: int
    team_id: Optional[int] = None
    match_id: Optional[int] = None

    class Config:
        from_attributes = True

# --- Standard Referee Output ---
class RefereeOut(BaseModel):
    id: int
    name: str
    country: Optional[str] = None

# --- Referee with Match Role ---
class RefereeWithRoleOut(RefereeOut):
    role: Optional[str] = None


class MatchBaseOut(BaseModel):
    id: int
    game_code: str
    championship_id: int
    team_a_id: int
    team_b_id: int
    team_a: Optional["TeamOut"] = None
    team_b: Optional["TeamOut"] = None

# --- Score + status output ---
class MatchScoreOut(MatchBaseOut):
    status: str
    team_a_score: Optional[Dict] = None
    team_b_score: Optional[Dict] = None

# --- States output ---
class MatchStatesOut(MatchBaseOut):
    team_a_stats: Optional[Dict] = None
    team_b_stats: Optional[Dict] = None


class PlayerStatsOut(BaseModel):
    match_id: int
    player_id: int
    team_id: int
    stats: Optional[Dict] = None


class ActionOut(BaseModel):
    Game: str
    Team: str
    Name: str
    Nr: str
    Text: str
    PLTime: str