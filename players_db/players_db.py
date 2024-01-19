import logging
from typing import Dict, Any, cast

from python_players.players_model.league import League
from python_players.players_model.player import Player
from python_players.players_model.team import Team


class PlayersDB:

    def __init__(self):
        self.players_collection = None
        self.teams_collection = None
        self.leagues_collection = None
        self.init_client()

    def init_client(self) -> Any:
        raise NotImplementedError

    @staticmethod
    def add_item(collection, item: Dict) -> Any:
        raise NotImplementedError

    @staticmethod
    def get_updated_dict(children_name: str, item_dict: Dict[str, Any], ids: Dict[str, Any]):
        for child_dict in item_dict[children_name]:
            child_dict["id"] = ids[child_dict["name"]]
        return item_dict

    def add_league_item(self, league: League) -> Any:
        ids = {}
        for team in league.children:
            ids[team.name] = self.add_team_item(cast(Team, team))
        league_dict = self.get_updated_dict(league.children_type_name(),
                                            league.to_dict(),
                                            ids)
        mongo_id = self.add_item(self.leagues_collection, league_dict)
        logging.debug(f"Added into MongoDB league {league.name} with ID={mongo_id}")
        return mongo_id

    def add_team_item(self, team: Team) -> Any:
        ids = {}
        for player in team.children:
            ids[player.name] = self.add_player_item(cast(Player, player))
        team_dict = self.get_updated_dict(team.children_type_name(),
                                          team.to_dict(),
                                          ids)

        mongo_id = self.add_item(self.teams_collection, team_dict)
        logging.debug(f"Added into MongoDB team {team.name} with ID={mongo_id}")
        return mongo_id

    def add_player_item(self, player: Player) -> Any:
        mongo_id = self.add_item(self.players_collection, player.to_dict())
        logging.debug(f"Added into MongoDB player {player.name} with ID={mongo_id}")
        return mongo_id
