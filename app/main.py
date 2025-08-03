import re
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from app.models import Game, GameList
from app.database import games_collection
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from typing import List
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.post("/games/batch")
def create_games(games: List[Game]):
    inserted = []
    skipped = []

    for game in games:
        # Check for existing game by title
        if games_collection.find_one({"title": game.title}):
            skipped.append(game.title)
            continue

        games_collection.insert_one(game.dict())
        inserted.append(game.title)

    return {
        "inserted": inserted,
        "skipped_duplicates": skipped,
        "message": f"{len(inserted)} games inserted, {len(skipped)} skipped"
    }


@app.get("/games")
def get_all_games():
    games = list(games_collection.find())
    for game in games:
        game["_id"] = str(game["_id"])
    return games


@app.get("/games/title/search")
def search_game_by_title(query: str = Query(..., min_length=1)):
    games = list(games_collection.find({
        "title": {"$regex": re.escape(query), "$options": "i"}
    }))
    for game in games:
        game["_id"] = str(game["_id"])
    return games



@app.get("/games/genre/search")
def search_games_by_genre(query: str = Query(..., min_length=1)):
    games = list(games_collection.find({
        "genre": {"$regex": re.escape(query), "$options": "i"}
    }))
    for game in games:
        game["_id"] = str(game["_id"])
    return games


@app.get("/games/platform/search")
def search_games_by_platform(query: str = Query(..., min_length=1)):
    games = list(games_collection.find({
        "platform": {"$regex": re.escape(query), "$options": "i"}
    }))
    for game in games:
        game["_id"] = str(game["_id"])
    return games


# FastAPI MCP
mcp = FastApiMCP(app, name="Game API MCP")
mcp.mount()