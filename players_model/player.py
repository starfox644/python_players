from typing import List
from .data_item import Field, DataItem


class Player(DataItem):

    def __init__(self):
        DataItem.__init__(self)

    def init_fields(self) -> List[Field]:
        return [
            Field(name="current_position", is_list=False),
            Field(name="number", is_list=False),
            Field(name="nationality", is_list=False),
            Field(name="preferred_foot", is_list=False),
            Field(name="preferred_positions", is_list=True),
            Field(name="age", is_list=False),
            Field(name="performance", is_list=False),
            Field(name="height", is_list=False),
            Field(name="weight", is_list=False),
        ]
