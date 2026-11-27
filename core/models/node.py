from attrs import define


@define
class Node:
    name: str
    price: int
    category: str
    id: str