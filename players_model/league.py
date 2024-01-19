from typing import List, Tuple
from .data_item import DataItem, Field


class League(DataItem):

    def __init__(self, full_name: str = ""):
        if full_name:
            name, country, division = self.strip_full_name(full_name)
        else:
            name = country = division = ""

        DataItem.__init__(self, name)
        self.country = country
        self.division = division

    def children_type_name(self) -> str:
        return "Teams"

    @staticmethod
    def strip_full_name(full_name: str) -> Tuple[str, str, str]:
        parts = full_name.split(" ")
        str_division = parts[-1]
        if str_division.startswith("("):
            name = " ".join(parts[1:-1])
            division = str_division[1]
            country = full_name.split(" ")[0]
        else:
            division = country = ""
            name = full_name

        return name, country, division

    def init_fields(self) -> List[Field]:
        return [
            Field(name="country", is_list=False),
            Field(name="division", is_list=False)
        ]
