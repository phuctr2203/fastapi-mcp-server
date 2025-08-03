from pydantic import BaseModel
from typing import Optional, List

class Game(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: int
    developer: Optional[str] = None

class GameList(BaseModel):
    games: List[Game]