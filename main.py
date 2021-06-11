import os
import tempfile
import time
import validators
from telethon import TelegramClient, events, sync
from telethon import functions, types
from telethon.tl.types import InputPhoto
from datetime import datetime

# You must get your own api_id and api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

def get_path_or_url(path_or_url):
    try:
        if validators.url(path_or_url):
            local_filename = tempfile.TemporaryFile()
            r = requests.get(url)
            f = open(local_filename, 'wb')
            for chunk in r.iter_content(chunk_size=512 * 1024): 
                if chunk:
                    f.write(chunk)
            f.close()
            return path_or_url
        elif os.path.exists(path_or_url):
            return path_or_url
        raise Exception
    except:
        print(f"[-] Error while processing file: {path_or_url}. Check if it is a file path or a working url to the image/video you want")

OFFLINE_IMAGE_PATH = get_path_or_url(os.getenv("OFFLINE_IMAGE_PATH"))
ONLINE_IMAGE_PATH = get_path_or_url(os.getenv("ONLINE_IMAGE_PATH"))

client = TelegramClient('bio_session', api_id, api_hash)
client.start()

async def do():
    # me = await client.get_me()
    _online = True
    while 1:
        print("Checking ....",end="\t")
        me = await client.get_me()
        # print(me)
        if "online" in (me.status.to_dict()["_"]).lower():
            print("is online")
            if not _online:
                print("Setting Profile: Online")
                p = await client.get_profile_photos('me')
                p = p[0]
                await client(functions.photos.DeletePhotosRequest(
                    id=[InputPhoto(
                        id=p.id,
                        access_hash=p.access_hash,
                        file_reference=p.file_reference
                    )]
                ))
                _online  = 1
                image = await client.upload_file(ONLINE_IMAGE_PATH)
                await client(functions.photos.UploadProfilePhotoRequest(video=image))
        else:
            print("is offline")
            if _online:
                print("Setting Profile: Offline")
                p = await client.get_profile_photos('me')
                p = p[0]
                await client(functions.photos.DeletePhotosRequest(
                    id=[InputPhoto(
                        id=p.id,
                        access_hash=p.access_hash,
                        file_reference=p.file_reference
                    )]
                ))
                _online  = 0
                image = await client.upload_file(OFFLINE_IMAGE_PATH)
                await client(functions.photos.UploadProfilePhotoRequest(video=image))
        print(f"Sleeping for {5} seconds")
        time.sleep(5)

import asyncio
# asyncio.run(do())
loop = asyncio.get_event_loop()
task = loop.create_task(do())
loop.run_until_complete(task)
