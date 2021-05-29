import asyncio
from db import DB
from youtube import Youtube
import os


async def main():
    uri = os.getenv("MONGOURI", "mongodb://localhost:27017")
    keys = os.getenv('YOUTUBE_KEYS', '').split(' ')
    assert len(keys)!=0, 'pass YOUTUBE_KEYS'
    db = DB(uri=uri)
    yt = Youtube(keys=keys)
    while 1:
        try:
            videos = await yt.getvideos(
                {
                    "part": ["snippet"],
                    "type": "video",
                    "order": "date",
                    # 'publishedAfter': '',
                }
            )
            await db.save(videos)
            await asyncio.sleep(10)
        except Exception as e:
            print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
