from .orm import Team, Championship, TeamInChamp, Player, Match, Referee, RefereeInMatch, PlayerStats
from sqlalchemy.orm import Session
from fastapi import HTTPException


class Champ:

    def __init__(self, id: int, session: Session):
        self.id = id
        self.session = session
        existing = session.query(Championship).filter_by(id=id).first()
        self.champ_exists = False
        if existing:
            self.champ_exists = True
            self.championship=existing

    
    def _safe_int(self,value: int | str | None) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return -1


    def _safe_float(self,value: float | str | None)-> float:
        try:
            return float(value)
        except (ValueError, TypeError):
            return -1.0
        

    def _create_teams(self,parsed_data:dict[str,dict[str, str]], name=None, abbreviation=None) -> list[Team]:
        if (not name and abbreviation) or (name and not abbreviation):
            raise HTTPException(
                status_code=400, #Bad Request, which is appropriate since the client sent incomplete data.
                detail="Both name and abbreviation must be provided together."
            ) 
        
        if name and abbreviation:
            existing_team = self.session.query(Team).filter_by(abbreviation=abbreviation).first()
            if existing_team:
                return
            else:
                team = Team(name=name, abbreviation=abbreviation)
                self.session.add(team)
                self.session.commit()
                return [team]
            
        gameinfo = parsed_data["gameinfo"][0]

        teams_data = [
            {"name": gameinfo["TeamNameA"], "abbreviation": gameinfo["TIDA"]},
            {"name": gameinfo["TeamNameB"], "abbreviation": gameinfo["TIDB"]}
        ]

        result_teams = []
        for team_data in teams_data:
            existing_team = self.session.query(Team).filter_by(abbreviation=team_data["abbreviation"]).first()
            if not existing_team:
                team = Team(**team_data)
                result_teams.append(team)
                self.session.add(team)

        self.session.commit()
        return result_teams


    def _link_team_to_championship(self,team_abbr:str)-> None:
        team = self.session.query(Team).filter_by(abbreviation=team_abbr).first()
        if not team:
            raise HTTPException(status_code=404,detail=f"Team with abbreviation '{team_abbr}' not found.")

        existing_link = self.session.query(TeamInChamp).filter_by(team_id=team.id,championship_id=self.championship.id).first()

        if not existing_link:
            link = TeamInChamp(team_id=team.id, championship_id=self.championship.id)
            self.session.add(link)
            self.session.commit()


    def _add_match(self,parsed_data:dict[str,dict[str, str]]) -> Match:
        gameinfo = parsed_data["gameinfo"][0]
        game_code = gameinfo["Game"]
        # Check if match already exists
        existing_match = self.session.query(Match).filter_by(game_code=game_code , championship_id =self.championship.id).first()
        if existing_match:
            return existing_match

        # Extract game basic info
        status = gameinfo.get("GStatus")

        # Get team abbreviations
        team_a_abbr = gameinfo["TIDA"]
        team_b_abbr = gameinfo["TIDB"]

        # Get team scores
        team_a_score = {
            "total": self._safe_int(gameinfo["RA"]) ,
            "first_half": self._safe_int(gameinfo["RA1"]) ,
            "second_half": self._safe_int(gameinfo["RA2"]) 
        }

        team_b_score = {
            "total": self._safe_int(gameinfo["RB"]),
            "first_half": self._safe_int(gameinfo["RB1"]) ,
            "second_half": self._safe_int(gameinfo["RB2"]) 
        }

        # Find teams by abbreviation
        team_a = self.session.query(Team).filter_by(abbreviation=team_a_abbr).first()
        if not team_a:
            raise HTTPException(status_code=404,etail=f"Team '{team_a_abbr}' not found.")

        team_b = self.session.query(Team).filter_by(abbreviation=team_b_abbr).first()
        if not team_b:
            raise HTTPException(status_code=404,detail=f"Team '{team_b_abbr}' not found.")

        # Create match object
        match = Match(
            game_code=game_code,
            championship_id=self.championship.id,
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            team_a_score=team_a_score,
            team_b_score=team_b_score,
            status=status
        )

        self.session.add(match)
        self.session.commit()
        return match


    def _update_match_score(self,parsed_data: dict[str,dict[str, str]]) -> Match:
        gameinfo = parsed_data["gameinfo"][0]
        game_code = gameinfo["Game"]

        # Find the existing match
        match = self.session.query(Match).filter_by(game_code=game_code,championship_id =self.championship.id).first()
        if not match:
            return None

        match.team_a_score = {
        "total": self._safe_int(gameinfo.get("RA")),
        "first_half": self._safe_int(gameinfo.get("RA1")),
        "second_half": self._safe_int(gameinfo.get("RA2")),
        }

        match.team_b_score = {
            "total": self._safe_int(gameinfo.get("RB")),
            "first_half": self._safe_int(gameinfo.get("RB1")),
            "second_half": self._safe_int(gameinfo.get("RB2")),
        }

        self.session.commit()
        return match


    def _clean_stats(self,row: dict[str,dict[str, str]]) -> dict[str, int | float]:
        return {
            "all_goals": self._safe_int(row.get("AllG")),
            "all_shots": self._safe_int(row.get("AllShots")),
            "all_efficiency": self._safe_float(row.get("AllEff")),
            "goals_7m": self._safe_int(row.get("P7mG")),
            "eff_7m": self._safe_float(row.get("P7mEff")),
            "goals_9m": self._safe_int(row.get("P9mG")),
            "eff_9m": self._safe_float(row.get("P9mEff")),
            "goals_6m": self._safe_int(row.get("P6mG")),
            "eff_6m": self._safe_float(row.get("P6mEff")),
            "goals_near": self._safe_int(row.get("NearG")),
            "eff_near": self._safe_float(row.get("NearEff")),
            "goals_wing": self._safe_int(row.get("WingG")),
            "eff_wing": self._safe_float(row.get("WingEff")),
            "goals_fastbreak": self._safe_int(row.get("FBG")),
            "eff_fastbreak": self._safe_float(row.get("FBEff")),
            "yellow_cards": self._safe_int(row.get("YC")),
            "red_cards": self._safe_int(row.get("RC")),
            "blue_cards": self._safe_int(row.get("EX")),
            "suspensions_2min": self._safe_int(row.get("P2minT")),
            "total_7m_shots": self._safe_int(row.get("P7mShots")),
        }


    def _update_or_add_match_stats(self,parsed_data: dict[str,dict[str, str]]) -> Match:
        statteam = parsed_data.get("statteam", [])
        if not statteam or len(statteam) < 2:
            raise HTTPException(status_code=400,detail="Statteam data is incomplete or missing.")
        
        match_code = statteam[0].get("Game")
        match = self.session.query(Match).filter_by(game_code=match_code,championship_id =self.championship.id).first()
        if not match:
            raise HTTPException(status_code=404,detail=f"No match found with code '{match_code}'.")

        # Create a mapping from team code to team_id
        team_code_to_stats = {}
        for row in statteam:
            team_code = row.get("Team")
            stats = self._clean_stats(row)
            team_code_to_stats[team_code] = stats

        # Load actual teams from DB for this match
        team_a = match.team_a
        team_b = match.team_b

        # If teams don't exist (deleted or null), skip setting stats
        if not team_a or not team_b:
            return match
        # Make sure the teams exist in parsed data
        if team_a.abbreviation not in team_code_to_stats or team_b.abbreviation not in team_code_to_stats:
            return match
        
        match.team_a_stats = team_code_to_stats[team_a.abbreviation]
        match.team_b_stats = team_code_to_stats[team_b.abbreviation]

        self.session.commit()
        return match


    def _insert_referees(self,parsed_data: dict[str,dict[str, str]]) -> list[Referee]:
        
        referee_data = parsed_data.get("referee", [])
        if not referee_data:
            raise HTTPException(status_code=400, detail="No referee data found.")

        referee_entry = referee_data[0]
        game_code = referee_entry.get("Game")
        link_to_match = True

        if not game_code:
            link_to_match=False
        # Try to get the match if linking is requested
        match = None
        if link_to_match:
            match = self.session.query(Match).filter_by(game_code=game_code).first()
            if not match:
                raise HTTPException(status_code=404,detail=f"No match found for game code '{game_code}'.")

        # Prepare referee list
        referees_info = [
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

        created_or_found_refs = []

        for ref_info in referees_info:
            # Create or fetch referee
            referee = self.session.query(Referee).filter_by(name=ref_info["name"],country=ref_info["country"]).first()

            if not referee:
                referee = Referee(name=ref_info["name"],country=ref_info["country"])
                self.session.add(referee)
                self.session.flush()

            created_or_found_refs.append(referee)

            # Optionally link to match
            if link_to_match and match:
                self._link_referees_to_match(self.session, match, referee, ref_info["role"])

        self.session.commit()
        return created_or_found_refs


    def _link_referees_to_match(self,session: Session, match: Match, referee: Referee, role: str) -> None:
        """Links a referee to a match if not already linked."""
     
        existing_link = session.query(RefereeInMatch).filter_by(match_id=match.id,referee_id=referee.id,).first()

        if not existing_link:
            match_ref_link = RefereeInMatch(match_id=match.id,referee_id=referee.id,role=role)
            session.add(match_ref_link)


    def _insert_players(self,parsed_data:dict[str,dict[str, str]]) -> None :
        statind = parsed_data.get("statind", [])

        if not statind:
            raise HTTPException(status_code=400,detail="No player data found in [statind].")

        for row in statind:
            first_name = row.get("FirstName")
            last_name = row.get("SurName")
            number = row.get("Nr")
            team_abbr = row.get("TID")

            if not (first_name and last_name and team_abbr):
                continue

            # Find team
            team = self.session.query(Team).filter_by(abbreviation=team_abbr).first()
            if not team:
                continue

            # Check if player exists
            existing_player = self.session.query(Player).filter_by(first_name=first_name,last_name=last_name,team_id=team.id).first()

            if not existing_player:
                new_player = Player(first_name=first_name,last_name=last_name,number=self._safe_int(number) ,team_id=team.id)
                self.session.add(new_player)

        self.session.commit()


    def _insert_player_stats(self,parsed_data:dict[str,dict[str, str]]) -> None:
        statind = parsed_data.get("statind", [])
        gameinfo = parsed_data.get("gameinfo", [])

        if not statind or not gameinfo:
            raise HTTPException(status_code=400,detail="Missing [statind] or [gameinfo] section.")

        game_code = gameinfo[0]["Game"]
        match = self.session.query(Match).filter_by(game_code=game_code,championship_id =self.championship.id).first()

        if not match:
            return

        for row in statind:
            first_name = row.get("FirstName")
            last_name = row.get("SurName")
            team_abbr = row.get("TID")

            if not (first_name and last_name and team_abbr):
                continue

            team = self.session.query(Team).filter_by(abbreviation=team_abbr).first()
            if not team:
                continue

            player = self.session.query(Player).filter_by(first_name=first_name,last_name=last_name,team_id=team.id).first()

            if not player:
                continue

            # Check if stats already exist
            existing = self.session.query(PlayerStats).filter_by(match_id=match.id,player_id=player.id).first()

            if existing:
                continue

            stats_json = {
                "all_goals": self._safe_int(row.get("AllG")),
                "shots_efficiency": self._safe_float(row.get("AllEff")),
                "yellow_cards": self._safe_int(row.get("YC")),
                "red_cards": self._safe_int(row.get("RC")),
                "blue_cards": self._safe_int(row.get("EX")),
                "suspensions_2min": self._safe_int(row.get("P2minT"))
            }

            player_stats = PlayerStats(match_id=match.id,player_id=player.id,team_id=team.id,stats=stats_json)
            self.session.add(player_stats)

        self.session.commit()


    def _update_player_stats(self,parsed_data: dict[str,dict[str, str]]) -> None:
        statind = parsed_data.get("statind", [])
        gameinfo = parsed_data.get("gameinfo", [])

        if not statind or not gameinfo:
            raise HTTPException(status_code=400,detail="Missing [statind] or [gameinfo] section.")

        game_code = gameinfo[0]["Game"]
        match = self.session.query(Match).filter_by(game_code=game_code,championship_id =self.championship.id).first()

        if not match:
            raise HTTPException(status_code=404,detail=f"Match {game_code} not found.")

        for row in statind:
            first_name = row.get("FirstName")
            last_name = row.get("SurName")
            team_abbr = row.get("TID")

            if not (first_name and last_name and team_abbr):
                continue

            team = self.session.query(Team).filter_by(abbreviation=team_abbr).first()
            if not team:
                continue

            player = self.session.query(Player).filter_by(first_name=first_name,last_name=last_name,team_id=team.id).first()

            if not player:
                continue

            existing = self.session.query(PlayerStats).filter_by(match_id=match.id,player_id=player.id).first()

            if not existing:
                continue

            # Update stats
            existing.stats = {
                "all_goals": self._safe_int(row.get("AllG")),
                "shots_efficiency": self._safe_float(row.get("AllEff")),
                "yellow_cards": self._safe_int(row.get("YC")),
                "red_cards": self._safe_int(row.get("RC")),
                "blue_cards": self._safe_int(row.get("EX")),
                "suspensions_2min": self._safe_int(row.get("P2minT"))
            }

        self.session.commit()


    def _parsed_before(self, parsed_data: dict[str,dict[str, str]]) -> bool:
        """Check if the parsed data has been processed before."""
        if not self.champ_exists:
            raise HTTPException(status_code=404,detail=f"Championship{self.id} does not exist. Please create it first.")
        
        gameinfo = parsed_data.get("gameinfo", [])
        if not gameinfo:
            return False
        game_code = gameinfo[0].get("Game")
        if not game_code:
            return False
        existing_match = self.session.query(Match).filter_by(game_code=game_code, championship_id=self.championship.id).first()
        return existing_match is not None


    def _add_data(self, parsed_data: dict[str,dict[str, str]]) -> None:
        """Main method to add parsed data to the database."""
        # Create teams
        self._create_teams(parsed_data)

        # Link teams to championship
        team_a= parsed_data["gameinfo"][0]["TIDA"]
        team_b= parsed_data["gameinfo"][0]["TIDB"]

        self._link_team_to_championship(team_a)
        self._link_team_to_championship(team_b)

        # Add match
        self._add_match(parsed_data)
        
        # Insert referees
        self._insert_referees(parsed_data)

        # Insert players
        self._insert_players(parsed_data)

        # Insert player stats
        self._insert_player_stats(parsed_data)

        # add match stats
        self._update_or_add_match_stats(parsed_data)


    def _update_data(self, parsed_data: dict[str,dict[str, str]]) -> None:
        """Main method to update parsed data in the database."""

        # Update match score
        self._update_match_score(parsed_data)

        # Update match stats
        self._update_or_add_match_stats(parsed_data)

        # Update player stats
        self._update_player_stats(parsed_data)
    
    
    def process_data(self, parsed_data: dict[str,dict[str, str]]) -> None:
        """Process parsed data based on whether it has been processed before."""
        if self._parsed_before(parsed_data):
            self._update_data(parsed_data)
        else:
            self._add_data(parsed_data)

