from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    title: str
    author: str
    genre: str
    year: int
    description: str
    read: bool = False
    favorite: bool = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
