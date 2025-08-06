-- Drop tables if they exist to start with a clean slate
DROP TABLE IF EXISTS player_stats, team_stats, referees, players, teams, matches, championships, team_in_champ , referee_in_match CASCADE;

-- Table for Championships
CREATE TABLE championships (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE
);

-- Table for Teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10)NOT NULL UNIQUE
);

CREATE TABLE team_in_champ (
    team_id INT NOT NULL,
    championship_id INT NOT NULL,

    -- Define Foreign Keys first
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (championship_id) REFERENCES championships(id) ON DELETE CASCADE,

    -- Define the Primary Key as the combination of the two foreign keys
    PRIMARY KEY (team_id, championship_id)
);
-- Table for Players
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    "Number" INT, -- Quoted because Number can be a reserved keyword
    team_id INT,
    UNIQUE (first_name, last_name, team_id),
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- Table for Matches
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    game_code VARCHAR(50) UNIQUE,
    "date" DATE, -- Quoted because date is a type name
    championship_id INT,
    team_a_id INT,
    team_b_id INT,
    score_a INT,
    score_b INT,
    score_a_1st_half INT,
    score_b_1st_half INT,
    score_a_2nd_half INT,
    score_b_2nd_half INT,
    status VARCHAR(50),
    FOREIGN KEY (championship_id) REFERENCES championships(id) ON DELETE CASCADE,
    FOREIGN KEY (team_a_id) REFERENCES teams(id) ON DELETE SET NULL,
    FOREIGN KEY (team_b_id) REFERENCES teams(id) ON DELETE SET NULL
);

-- Table for Referees
CREATE TABLE referees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(100)
);

CREATE TABLE referee_in_match (
    match_id INT NOT NULL,
    referee_id INT NOT NULL,
    role VARCHAR(100) NOT NULL, -- The role is specific to this match

    -- Define Foreign Keys first
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (referee_id) REFERENCES referees(id) ON DELETE CASCADE,

    -- Define the Primary Key to ensure a referee can't have two roles in the same match
    PRIMARY KEY (match_id, referee_id)
);

-- Table for Player Statistics
CREATE TABLE player_stats (
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    all_goals INT,
    shots_efficiency FLOAT,
    yellow_cards INT,
    red_cards INT,
    blue_cards INT,
    suspensions_2min INT,
    PRIMARY KEY (match_id, player_id),
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);

-- Table for Team Statistics
CREATE TABLE team_stats (
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    --stats_details JSONB, -- Store detailed stats as JSON
    all_goals INT,
    all_shots INT,
    all_efficiency FLOAT,
    goals_7m INT,
    eff_7m FLOAT,
    goals_9m INT,
    eff_9m FLOAT,
    goals_6m INT,
    eff_6m FLOAT,
    goals_near INT,
    eff_near FLOAT,
    goals_wing INT,
    eff_wing FLOAT,
    goals_fastbreak INT,
    eff_fastbreak FLOAT,
    yellow_cards INT,
    red_cards INT,
    blue_cards INT,
    suspensions_2min INT,
    total_7m_shots INT,
    PRIMARY KEY (match_id, team_id),
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
);