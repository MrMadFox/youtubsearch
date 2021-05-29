from aiohttp import ClientSession
from datetime import datetime


class Youtube:
    def __init__(self, keys):
        self.keys = keys

    @staticmethod
    async def get_quota(key):
        # TODO: get quota limit from quota apis
        return 1

    async def get_key(self):
        for key in self.keys:
            if await self.get_quota(key):
                return key
        raise Exception("quota limit reached for all keys")

    async def getvideos(self, params):
        async with ClientSession() as http_session:
            res = await (
                await http_session.get(
                    "https://youtube.googleapis.com/youtube/v3/search",
                    headers={"Accept": "application/json"},
                    params={"key": await self.get_key(), **params},
                )
            ).json()
        videos = []
        for item in res["items"]:
            thumbnails = {}
            for k, v in item["snippet"]["thumbnails"].items():
                thumbnails[k] = v["url"]
            
            videos.append(
                {
                    "publishedAt": datetime.fromisoformat(
                        item["snippet"]["publishedAt"][:-1]
                    ),
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channelTitle": item["snippet"]["channelTitle"],
                    "_id": item["id"]["videoId"],
                    "thumbnails": thumbnails
                }
            )
        return videos
