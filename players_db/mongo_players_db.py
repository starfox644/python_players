import bson
import pymongo
from bson.objectid import ObjectId
from typing import Any, Dict, Union
from collections.abc import Iterable
from .players_db import PlayersDB


class MongoPlayersDB(PlayersDB):

    def __init__(self):
        PlayersDB.__init__(self)

    def init_client(self) -> Any:
        client = pymongo.MongoClient("mongodb://51.38.82.47:27017/players",
                                     username='fox',
                                     password='e9dqnyPl6wdBhiP',
                                     )
        mydb = client["players"]
        self.leagues_collection = mydb["Leagues"]
        self.teams_collection = mydb["Teams"]
        self.players_collection = mydb["Players"]

    def reset_db(self):
        self.leagues_collection.drop()
        self.teams_collection.drop()
        self.players_collection.drop()

    @staticmethod
    def add_item(collection, item: Dict) -> bson.objectid.ObjectId:
        inserted = collection.insert_one(item)
        return inserted.inserted_id

    @staticmethod
    def get_item(collection, item_id: Union[ObjectId, str]):
        if isinstance(item_id, str):
            item_id = ObjectId(item_id)
        return next(collection.find({"_id": item_id}))

    def get_leagues(self):
        return list(self.leagues_collection.find())

    def get_league(self, league_id: Union[ObjectId, str]):
        return self.get_item(self.leagues_collection, league_id)

    def get_team(self, team_id: Union[ObjectId, str]):
        return self.get_item(self.teams_collection, team_id)

    def get_player(self, player_id: Union[ObjectId, str]):
        return self.get_item(self.players_collection, player_id)

    @staticmethod
    def replace_object_ids(data: Any):
        if isinstance(data, Dict):
            for key, value in data.items():
                data[key] = MongoPlayersDB.replace_object_ids(value)
        elif isinstance(data, Iterable) and not isinstance(data, str):
            data = [MongoPlayersDB.replace_object_ids(value) for value in data]
        elif isinstance(data, ObjectId):
            return str(data)
        return data
