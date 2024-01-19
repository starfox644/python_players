from typing import List
from .data_item import DataItem, Field


class Team(DataItem):

    def __init__(self):
        DataItem.__init__(self)

    def children_type_name(self) -> str:
        return "Players"

    def init_fields(self) -> List[Field]:
        return []
