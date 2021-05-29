from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
import asyncio

class DB:
    def __init__(self, uri="mongodb://mongo:27017"):
        self.uri = uri
        self.initialized = False

    def initialize(self):
        if self.initialized: return
        client = MotorClient(self.uri)
        self.collection = client["prod"]["videos"]
        self.collection.create_index("publishedAt")
        self.initialized = True

    async def save(self, videos: Dict):
        self.initialize()
        tasks = [asyncio.ensure_future(self.collection.insert_one(video)) for video in videos]
        for task in tasks:
            try:
                await task
            except Exception as err:
                if err.code != 11000: raise
                print('error while saving', err)

    async def get(self, query={}, page=1, limit=10):
        self.initialize()
        result = []
        cursor = (
            self.collection.find(query, {"_id": 0})
            .sort("publishedAt")
            .limit(limit).skip((page - 1) * limit)
        )
        async for document in cursor:
            result.append(document)
        return result
