from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Date,
    ForeignKey, JSON, UniqueConstraint, Index , cast
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from dotenv import load_dotenv
import os

# Load .env
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

# --- Join Table: Team in Championship ---
class TeamInChamp(Base):
    __tablename__ = "team_in_champ"

    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    championship_id = Column(Integer, ForeignKey("championships.id", ondelete="CASCADE"), primary_key=True)

    team = relationship("Team", back_populates="team_champ_links")
    championship = relationship("Championship", back_populates="team_champ_links")

# --- Team ---
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10), nullable=False, unique=True)

    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")

    team_champ_links = relationship("TeamInChamp", back_populates="team", cascade="all, delete-orphan")
    championships = relationship("Championship", secondary="team_in_champ", back_populates="teams")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', abbr='{self.abbreviation}')>"

# --- Championship ---
class Championship(Base):
    __tablename__ = "championships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    team_champ_links = relationship("TeamInChamp", back_populates="championship", cascade="all, delete-orphan")
    teams = relationship("Team", secondary="team_in_champ", back_populates="championships")

    matches = relationship("Match", back_populates="championship", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Championship(id={self.id}, name='{self.name}')>"

# --- Player ---
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    number = Column("Number", Integer)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"))

    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("first_name", "last_name", "team_id"),
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.first_name} {self.last_name}', number={self.number})>"

# --- Match ---
class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("game_code", "championship_id", name="unique_game_in_championship"),
    )

    id = Column(Integer, primary_key=True)
    game_code = Column(String(50), nullable=False)  # Removed unique=True
    championship_id = Column(Integer, ForeignKey("championships.id", ondelete="CASCADE"), nullable=False)
    team_a_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"))
    team_b_id = Column(Integer, ForeignKey("teams.id", ondelete="SET NULL"))
    team_a_score = Column(JSON)
    team_b_score = Column(JSON)
    status = Column(String(50))
    team_a_stats = Column(JSON)
    team_b_stats = Column(JSON)

    championship = relationship("Championship", back_populates="matches")
    team_a = relationship("Team", foreign_keys=[team_a_id])
    team_b = relationship("Team", foreign_keys=[team_b_id])

    referees = relationship("RefereeInMatch", back_populates="match", cascade="all, delete-orphan")
    player_stats = relationship("PlayerStats", back_populates="match", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="match", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Match(id={self.id}, code='{self.game_code}', status='{self.status}')>"

# --- Referee ---
class Referee(Base):
    __tablename__ = "referees"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(String(100))

    matches = relationship("RefereeInMatch", back_populates="referee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Referee(id={self.id}, name='{self.name}', country='{self.country}')>"

# --- Join Table: Referee in Match ---
class RefereeInMatch(Base):
    __tablename__ = "referee_in_match"

    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), primary_key=True)
    referee_id = Column(Integer, ForeignKey("referees.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(100), nullable=False)

    match = relationship("Match", back_populates="referees")
    referee = relationship("Referee", back_populates="matches")

    def __repr__(self):
        return f"<RefereeInMatch(match_id={self.match_id}, referee_id={self.referee_id}, role='{self.role}')>"

# --- Player Stats ---
class PlayerStats(Base):
    __tablename__ = "player_stats"

    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))

    stats = Column(JSON)

    match = relationship("Match", back_populates="player_stats")
    player = relationship("Player", back_populates="stats")
    team = relationship("Team")

    def __repr__(self):
        return f"<PlayerStats(match_id={self.match_id}, player_id={self.player_id})>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    data = Column(JSONB, nullable=False)

    match = relationship("Match", back_populates="actions")

    __table_args__ = (Index("ix_actions_data_time",cast(data["Time"].astext, Integer)),
                      Index("ix_actions_data_pos", data["Pos"].astext))

    def __repr__(self):
        return f"<Action(id={self.id}, match_id={self.match_id})>"


# --- Create all tables ---
Base.metadata.create_all(bind=engine)
