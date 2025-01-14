#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 vasusen-code ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/vasusen-code/VIDEOconvertor/blob/public/LICENSE> .

import os
import time
import subprocess
import asyncio
from datetime import datetime as dt
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata
from telethon import events

def hhmmss(seconds):
    x = time.strftime('%H:%M:%S',time.gmtime(seconds))
    return x

async def ssgen(video, time_stamp):
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{hhmmss(time_stamp)}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
        
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       
        
async def screenshot(event, msg):
    Drone = event.client
    name = dt.now().isoformat("_", "seconds") + ".mp4"
    edit = await Drone.send_message(event.chat_id, "Trying to process.", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    if msg.file.name:
        name = msg.file.name
    try:
        await fast_download(name, file, Drone, edit, time.time(), "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading.") 
    pictures = []
    captions = []
    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    duration = (video_metadata(name))["duration"]
    for i in range(50):
        sshot = await ssgen(name, duration/n[i]) 
        if sshot is not None:
            pictures.append(sshot)
            captions.append(f'screenshot at {hhmmss(duration/n[i])}')
            await edit.edit(f"`{i+1}` screenshot generated.")
    if len(pictures) > 0:
        await Drone.send_file(event.chat_id, pictures, caption=captions)
    else:
        await edit.edit("No screenshots could be generated!")
    await edit.delete()
    for pic in pictures:
        os.remove(pic)
    os.remove(name)
