from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Adresse:
    adresseId: int
    name: str


@dataclass
class Bewertung:
    bewertungId: int
    name: str
    points: int
    text: str





@dataclass
class User:
    userid: int
    name: str
    email: str
    password: str


@dataclass
class Trainer:
    trainerId: int
    name: str
    email: str
    image_url: str
    birthday: str
    bewertung: Optional[Bewertung] = None



@dataclass
class Halle:
    halleId: int
    name: str
    image_url: str
    opening_time: datetime
    address: Adresse
    bewertung: Optional[Bewertung] = None



