from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime 


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
    id: str


# --- Token Models ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# --- Team Model ---

class Team(BaseModel):
    id: str
    name: str
    country: str


# --- Championship Models ---

class ChampionshipBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    teams: List[Team]


class ChampionshipCreate(ChampionshipBase):
    pass


class ChampionshipUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    teams: Optional[List[Team]]


class ChampionshipOut(ChampionshipBase):
    id: str
