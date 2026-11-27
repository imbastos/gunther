from attrs import define


@define
class Category:
    name: str
    color: str
    id: str