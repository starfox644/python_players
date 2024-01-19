from dataclasses import dataclass
from typing import List, Any


@dataclass
class Field:
    name: str
    is_list: bool
    value: Any = ""

    def __hash__(self):
        return hash(self.name)

    def __post_init__(self):
        if self.is_list and not self.value:
            self.value = []


class DataItem:

    def __init__(self, name: str = ""):
        self.__fields = {field.name: field for field in self.init_fields()}
        self.__fields["name"] = Field(name="name", is_list=False, value=name)
        self.children: List[DataItem] = []

    def init_fields(self) -> List[Field]:
        raise NotImplementedError

    def children_type_name(self) -> str:
        raise NotImplementedError

    def is_valid(self) -> bool:
        return bool(self.name)

    def get_field_names(self):
        for key in self.__fields.keys():
            yield key

    def add_child(self, child: 'DataItem'):
        self.children.append(child)

    def to_dict(self):
        result = {key: self.__fields[key].value for key in self.__fields}
        if self.children:
            result[self.children_type_name()] = [{"name": child.name} for child in self.children]
        return result

    def __getattr__(self, key):
        if key == "_DataItem__fields":
            return self.__dict__["__fields"]
        elif key in self.__fields:
            return self.__fields[key].value
        else:
            return self.__dict__[key]

    def __setattr__(self, key, value):
        if key == "_DataItem__fields":
            self.__dict__["__fields"] = value
        elif "__fields" in self.__dict__ and key in self.__fields:
            self.__fields[key].value = value
        else:
            self.__dict__[key] = value
