import bson
import pymongo
from bson.objectid import ObjectId
from typing import Any, Dict
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

    def get_leagues_names(self):
        return [league["name"] for league in self.leagues_collection.find()]

    def get_league(self, league_id: str):
        return self.leagues_collection.find({"id": league_id})

    def get_player(self, player_id: str):
        return next(self.players_collection.find({"_id": ObjectId(player_id)}))
