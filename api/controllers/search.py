from pydantic import BaseModel, Field
from typing import Dict
from fastapi import APIRouter
from .db import DB
import os

uri = os.getenv("MONGOURI", "mongodb://localhost:27017")

db = DB(uri)
router = APIRouter()


class SearchRequest(BaseModel):
    query: Dict = Field({})
    page: int = Field(1)
    limit: int = Field(10)


@router.on_event("startup")
async def initializing():
    db.initialize()


@router.post("/")
async def search(req: SearchRequest):
    res = await db.get(req.query, req.page, req.limit)
    return res
